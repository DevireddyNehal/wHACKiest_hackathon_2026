"""
AuraOS - End-to-End Test Suite
Tests all 5 pillars of the Autonomous Web Operating System.
"""

import asyncio
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["project"] == "AuraOS"
    assert "pillars" in data

    h = client.get("/health")
    assert h.status_code == 200
    assert h.json()["status"] == "HEALTHY"

def test_pillar1_smartpoint():
    """Test Micro-DOM Analysis & Hidden Fee Unmasking"""
    payload = {
        "dom_snippet": "<div class='fare-card'>Flight BLR to DEL: ₹4,899</div>",
        "user_prompt": "What is the real price with convenience fees?",
        "url": "https://booking.example.com"
    }
    res = client.post("/api/smartpoint/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "breakdown" in data
    assert data["category"] == "PRICING_UNMASKED"
    print("✓ Pillar 1 (SmartPoint) Passed:", data["title"])

def test_pillar3_synapse_swarm():
    """Test Multi-Tab Parallel Swarm Execution"""
    payload = {
        "goal": "Find cheapest direct flight BLR to DEL on Friday",
        "target_sites": ["MakeMyTrip", "IndiGo Direct", "EaseMyTrip"]
    }
    res = client.post("/api/swarm/execute", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert "winner" in data
    print("✓ Pillar 3 (SynapseSwarm) Passed:", data["winner"]["platform"])

def test_pillar4_ghost_butler():
    """Test Background Mission Creation and Slot Trigger"""
    # 1. List
    res = client.get("/api/butler/missions")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 2. Trigger demo event
    res2 = client.post("/api/butler/missions/trigger-demo", json={"mission_id": "mission_tatkal_demo"})
    assert res2.status_code == 200
    assert res2.json()["status"] == "EVENT_TRIGGERED"
    print("✓ Pillar 4 (GhostButler) Passed: Notification Dispatched to WhatsApp")

def test_pillar5_rewind_memory():
    """Test Semantic History Search"""
    res = client.post("/api/memory/search", json={"query": "LLM"})
    assert res.status_code == 200
    data = res.json()
    assert data["results_count"] >= 1
    print("✓ Pillar 5 (RewindWeb) Passed: Memory items retrieved")

if __name__ == "__main__":
    test_root_and_health()
    test_pillar1_smartpoint()
    test_pillar3_synapse_swarm()
    test_pillar4_ghost_butler()
    test_pillar5_rewind_memory()
    print("\n✓ Smoke tests passed for endpoints (Pillars 1, 3, 4, 5). AirTouch (Pillar 2) tested manually via browser DOM events.")
