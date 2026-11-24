"""GhostButler demo missions. Events are simulated and never book or send payments."""

import datetime
import uuid
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

router = APIRouter(prefix="/api/butler", tags=["GhostButler"])

ACTIVE_MISSIONS: Dict[str, Dict[str, Any]] = {
    "mission_demo_watch": {
        "id": "mission_demo_watch",
        "title": "Sample availability reminder",
        "portal": "Demo portal (no external site is monitored)",
        "trigger_condition": "Manual demo trigger only",
        "status": "DEMO_READY",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "demo_only": True,
    }
}


class CreateMissionRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    target_url: str = Field(min_length=1, max_length=300)
    condition: str = Field(min_length=1, max_length=200)
    scheduled_for: datetime.datetime | None = None

    @field_validator("scheduled_for")
    @classmethod
    def require_timezone_for_schedule(
        cls, value: datetime.datetime | None
    ) -> datetime.datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("Scheduled time must include a timezone.")
        return value


class TriggerMissionRequest(BaseModel):
    mission_id: str = Field(min_length=1, max_length=80)
    confirmed: bool = False


@router.get("/missions")
async def list_missions() -> List[Dict[str, Any]]:
    """List demo reminders held in this process; there is no background scheduler."""
    return list(ACTIVE_MISSIONS.values())


@router.post("/missions/create")
async def create_mission(req: CreateMissionRequest) -> Dict[str, Any]:
    """Create an in-memory reminder configuration, not an active booking monitor."""
    mission_id = f"mission_{uuid.uuid4().hex[:8]}"
    mission = {
        "id": mission_id,
        "title": req.title.strip(),
        "portal": req.target_url.strip(),
        "trigger_condition": req.condition.strip(),
        "scheduled_for": req.scheduled_for.isoformat() if req.scheduled_for else None,
        "status": "SCHEDULED_DEMO" if req.scheduled_for else "DEMO_READY",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "demo_only": True,
    }
    if not mission["title"] or not mission["portal"] or not mission["trigger_condition"]:
        raise HTTPException(status_code=422, detail="Mission fields cannot be blank.")
    ACTIVE_MISSIONS[mission_id] = mission
    return {"status": "CREATED_DEMO", "mission": mission}


@router.post("/missions/trigger-demo")
async def trigger_demo_event(req: TriggerMissionRequest) -> Dict[str, Any]:
    """Show an in-app alert preview after explicit confirmation; no external action occurs."""
    if not req.confirmed:
        raise HTTPException(
            status_code=409,
            detail="Confirm the demo alert in the interface before triggering it.",
        )
    mission = ACTIVE_MISSIONS.get(req.mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Demo reminder not found.")
    scheduled_for = mission.get("scheduled_for")
    if scheduled_for:
        due_at = datetime.datetime.fromisoformat(scheduled_for)
        if due_at > datetime.datetime.now(datetime.timezone.utc):
            raise HTTPException(
                status_code=409,
                detail="This demo reminder is scheduled for later and is not due yet.",
            )

    mission["status"] = "DEMO_ALERT_READY"
    message = (
        f"Demo event for “{mission['title']}”. This is a local preview only: "
        "no site was checked, no slot was held, and no booking or payment was made."
    )
    return {
        "status": "DEMO_EVENT_TRIGGERED",
        "mission": mission,
        "notification": {
            "status": "IN_APP_PREVIEW",
            "channel": "In-app demo",
            "recipient": None,
            "message": message,
        },
    }
