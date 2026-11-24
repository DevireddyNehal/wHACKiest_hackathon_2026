"""Focused API smoke and safety tests for the AuraOS demo."""

import sys
from pathlib import Path

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


if __name__ == "__main__":
    tests = [
        test_dashboard_and_health,
        test_smartpoint_uses_only_submitted_context,
        test_synapse_is_explicitly_simulated,
        test_ghostbutler_requires_confirmation_and_never_books,
        test_rewind_has_empty_state_and_explicit_capture,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
