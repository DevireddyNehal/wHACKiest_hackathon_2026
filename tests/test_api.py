"""Focused API smoke and safety tests for the AuraOS demo."""

import os
import sys
import tempfile
from pathlib import Path

os.environ["AURAOS_DATA_DIR"] = tempfile.mkdtemp(prefix="auraos-test-")

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.main import app

client = TestClient(app)


def test_dashboard_and_health():
    page = client.get("/")
    assert page.status_code == 200
    assert "AuraOS" in page.text
    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.json()["demo_mode"] is True
    assert client.get("/health").json()["status"] == "HEALTHY"


def test_smartpoint_uses_only_submitted_context():
    response = client.post(
        "/api/smartpoint/analyze",
        json={
            "dom_snippet": "<div>Base fare ₹4,899 · fee ₹250</div>",
            "user_prompt": "Check the total",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "PRICING_UNMASKED"
    assert data["analysis_mode"] == "DEMO_MOCK"
    assert "cannot verify" in data["summary"]
    assert "₹1,950" not in str(data)
    limited = client.post(
        "/api/smartpoint/analyze",
        json={"dom_snippet": "Seat selected", "user_prompt": "Check the total fee"},
    ).json()
    assert limited["title"] == "Pricing question · limited excerpt"
    assert client.post(
        "/api/smartpoint/analyze", json={"dom_snippet": "x" * 2501}
    ).status_code == 422
    assert client.post(
        "/api/smartpoint/analyze", json={"dom_snippet": "   "}
    ).status_code == 422


def test_synapse_is_explicitly_simulated():
    response = client.post(
        "/api/swarm/execute",
        json={"goal": "Compare demo flights", "target_sites": ["Site A", "Site B"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["execution_mode"] == "SIMULATED"
    assert data["prefilled_cart_ready"] is False
    assert "No websites were opened" in data["message"]
    assert client.post(
        "/api/swarm/execute", json={"goal": " ", "target_sites": ["Site A"]}
    ).status_code == 422
    pasted = client.post(
        "/api/swarm/execute",
        json={
            "goal": "Compare two pasted fares",
            "listings": [
                "Direct carrier\nBase fare ₹4,800",
                "Marketplace\nBase fare ₹4,899 · convenience fee ₹250",
            ],
        },
    )
    assert pasted.status_code == 200
    compared = pasted.json()
    assert compared["execution_mode"] == "FROM_USER_TEXT"
    assert compared["comparison_source"] == "USER_TEXT"
    assert compared["prefilled_cart_ready"] is False
    assert "₹6,849" not in str(compared)
    assert "₹250" in str(compared)
    assert "No websites were opened" in compared["message"]
    assert "checkout total" in " ".join(
        row["not_in_text"] for row in compared["comparison_matrix"]
    )
    assert compared["winner"]["platform"] == "Direct carrier"
    assert client.post(
        "/api/swarm/execute",
        json={"goal": "Too many snippets", "listings": ["a", "b", "c", "d"]},
    ).status_code == 422


def test_voice_commands_are_bounded_and_allowlisted():
    navigation = client.post(
        "/api/voice/command", json={"command": "Open the SynapseWeb screen!"}
    )
    assert navigation.status_code == 200
    assert navigation.json()["action"] == {"type": "navigate", "screen": "synapse"}

    search = client.post(
        "/api/voice/command", json={"command": "Search notes for hackathon"}
    ).json()
    assert search["action"] == {
        "type": "search_memory",
        "screen": "rewind",
        "query": "hackathon",
    }
    singular_search = client.post(
        "/api/voice/command", json={"command": "find memory for LLM"}
    ).json()
    assert singular_search["action"]["query"] == "llm"

    comparison = client.post(
        "/api/voice/command", json={"command": "run a comparison"}
    ).json()
    assert comparison["action"] == {"type": "run_comparison", "screen": "synapse"}

    snippet = client.post(
        "/api/voice/command", json={"command": "analyze the snippet"}
    ).json()
    assert snippet["action"] == {"type": "analyze_snippet", "screen": "smartpoint"}

    reminder = client.post(
        "/api/voice/command", json={"command": "Trigger demo alert"}
    ).json()
    assert reminder["action"] == {
        "type": "confirmation_required",
        "screen": "butler",
    }
    unsafe = client.post(
        "/api/voice/command", json={"command": "Book a ticket and pay"}
    ).json()
    assert unsafe["intent"] == "unknown"
    assert unsafe["action"]["type"] == "none"

    assert client.post(
        "/api/voice/command", json={"command": "   "}
    ).status_code == 422
    assert client.post(
        "/api/voice/command", json={"command": "x" * 251}
    ).status_code == 422


def test_local_speech_service_reports_engine_state():
    status = client.get("/api/voice/status")
    assert status.status_code == 200
    data = status.json()
    assert data["available"] is (data["engine"] == "local-vosk")
    assert data["engine"] in {"local-vosk", "typed-command-fallback"}

    with client.websocket_connect("/ws/speech") as websocket:
        message = websocket.receive_json()
        if data["available"]:
            assert message == {"type": "ready", "engine": "local-vosk"}
        else:
            assert message["type"] == "error"
            assert "typed commands" in message["message"]


def test_ghostbutler_requires_confirmation_and_never_books():
    mission_id = client.get("/api/butler/missions").json()[0]["id"]
    path = "/api/butler/missions/trigger-demo"
    payload = {"mission_id": mission_id}
    assert client.post(path, json=payload).status_code == 409
    response = client.post(path, json={**payload, "confirmed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DEMO_EVENT_TRIGGERED"
    assert data["notification"]["status"] == "IN_APP_PREVIEW"
    assert data["notification"]["recipient"] is None
    assert "no booking or payment was made" in data["notification"]["message"]
    assert client.post(
        path, json={"mission_id": "missing", "confirmed": True}
    ).status_code == 404
    scheduled = client.post(
        "/api/butler/missions/create",
        json={
            "title": "Scheduled demo reminder",
            "target_url": "Example portal",
            "condition": "Reminder time arrives",
            "scheduled_for": "2099-01-01T00:00:00+00:00",
        },
    )
    scheduled_id = scheduled.json()["mission"]["id"]
    assert client.post(
        path, json={"mission_id": scheduled_id, "confirmed": True}
    ).status_code == 409
    assert client.post(
        "/api/butler/missions/create",
        json={
            "title": "Invalid schedule",
            "target_url": "Example portal",
            "condition": "Reminder time arrives",
            "scheduled_for": "2099-01-01T00:00:00",
        },
    ).status_code == 422


def test_rewind_has_empty_state_and_explicit_capture():
    empty = client.post("/api/memory/search", json={"query": "not-in-demo-data"})
    assert empty.status_code == 200
    assert empty.json()["results"] == []

    saved = client.post(
        "/api/memory/capture",
        json={
            "title": "My test note",
            "url": "https://example.com/note",
            "snippet": "User-selected snippet for a memory test",
        },
    )
    assert saved.status_code == 200
    found = client.post("/api/memory/search", json={"query": "memory test"})
    assert found.json()["results_count"] == 1
    assert found.json()["results"][0]["demo"] is False

    from backend.routers import rewind_memory

    rewind_memory.MEMORY_INDEX[:] = [
        item for item in rewind_memory.MEMORY_INDEX if item.get("demo")
    ]
    assert client.post("/api/memory/search", json={"query": "memory test"}).json()["results"] == []
    rewind_memory.reload_saved_notes()
    reloaded = client.post("/api/memory/search", json={"query": "memory test"}).json()
    assert reloaded["results_count"] == 1
    assert reloaded["storage"] == "LOCAL_FILE"


if __name__ == "__main__":
    tests = [
        test_dashboard_and_health,
        test_smartpoint_uses_only_submitted_context,
        test_synapse_is_explicitly_simulated,
        test_voice_commands_are_bounded_and_allowlisted,
        test_local_speech_service_reports_engine_state,
        test_ghostbutler_requires_confirmation_and_never_books,
        test_rewind_has_empty_state_and_explicit_capture,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
