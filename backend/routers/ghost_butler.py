"""
AuraOS - GhostButler Router
Manages asynchronous background missions (Tatkal sniper, result tracker, price watcher)
and dispatches notifications directly to WhatsApp when complete.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import datetime
from backend.services.notification import notification_service

router = APIRouter(prefix="/api/butler", tags=["GhostButler"])

# In-memory mission store for active background tasks
ACTIVE_MISSIONS: Dict[str, Dict[str, Any]] = {
    "mission_tatkal_demo": {
        "id": "mission_tatkal_demo",
        "title": "IRCTC Tatkal 3AC Booking",
        "portal": "https://www.irctc.co.in/nget/train-search",
        "trigger_condition": "Seats Available > 0 at 10:00:00 AM IST",
        "passengers": ["Rahul Sharma", "Nehal Gupta"],
        "status": "MONITORING_ACTIVE",
        "auto_hold": True,
        "phone": "+919876543210",
        "created_at": datetime.datetime.now().isoformat()
    }
}

class CreateMissionRequest(BaseModel):
    title: str
    target_url: str
    condition: str
    phone_number: Optional[str] = "+919876543210"
    auto_hold: Optional[bool] = True

class TriggerMissionRequest(BaseModel):
    mission_id: str

@router.get("/missions")
async def list_missions():
    """Lists all active and completed background GhostButler missions."""
    return list(ACTIVE_MISSIONS.values())

@router.post("/missions/create")
async def create_mission(req: CreateMissionRequest):
    """Assigns a new standing mission to GhostButler (e.g., watch slot, snipe ticket)."""
    mission_id = f"mission_{uuid.uuid4().hex[:8]}"
    mission = {
        "id": mission_id,
        "title": req.title,
        "portal": req.target_url,
        "trigger_condition": req.condition,
        "status": "MONITORING_ACTIVE",
        "auto_hold": req.auto_hold,
        "phone": req.phone_number,
        "created_at": datetime.datetime.now().isoformat()
    }
    ACTIVE_MISSIONS[mission_id] = mission
    return {"status": "SUCCESS", "mission": mission}

@router.post("/missions/trigger-demo")
async def trigger_demo_event(req: TriggerMissionRequest):
    """
    Simulates a background event completing while the user's laptop is closed.
    Triggers slot reserve and dispatches instant WhatsApp alert.
    """
    mission = ACTIVE_MISSIONS.get(req.mission_id)
    if not mission:
        mission = list(ACTIVE_MISSIONS.values())[0]

    mission["status"] = "SLOT_SECURED_ACTION_REQUIRED"

    # Send WhatsApp notification
    alert = await notification_service.send_whatsapp_alert(
        to_phone=mission.get("phone", "+919876543210"),
        title=f"Slot Secured: {mission['title']}",
        message=f"Tatkal booking opened! GhostButler secured 2 seats (Coach B3, 21-22). Total: ₹2,450. Held for 4 minutes.",
        action_url="https://pay.upi.example.com/approve/irctc_94812"
    )

    return {
        "status": "EVENT_TRIGGERED",
        "mission": mission,
        "notification": alert
    }
