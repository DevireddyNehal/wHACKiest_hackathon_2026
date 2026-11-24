"""
AuraOS - SynapseWeb Multi-Tab Swarm Router
Endpoint for parallel multi-site web automation, comparison, and form pre-fill.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from backend.services.llm_service import llm_service

router = APIRouter(prefix="/api/swarm", tags=["SynapseSwarm"])

class SwarmRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=300)
    target_sites: Optional[List[str]] = Field(default=None, max_length=5)
    max_parallel_tabs: int = Field(default=3, ge=1, le=5)

    @field_validator("goal")
    @classmethod
    def require_nonblank_goal(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Comparison goal cannot be blank.")
        return value

    @field_validator("target_sites")
    @classmethod
    def validate_sites(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        sites = [site.strip() for site in value if site.strip()]
        if not sites or any(len(site) > 100 for site in sites):
            raise ValueError("Provide up to five nonblank site labels of at most 100 characters.")
        return sites

class SwarmResponse(BaseModel):
    swarm_id: str
    goal: str
    status: str
    sites_scanned: List[str]
    winner: Dict[str, Any]
    comparison_matrix: List[Dict[str, Any]]
    prefilled_cart_ready: bool
    consent_shield_active: bool
    execution_mode: str
    message: str

@router.post("/execute", response_model=SwarmResponse)
async def execute_swarm_task(req: SwarmRequest):
    """
    Executes a parallel swarm across 3-4 competitor sites (e.g. Apollo vs 1mg vs Blinkit,
    or MakeMyTrip vs IndiGo vs EaseMyTrip) and synthesizes a single unified card.
    """
    default_sites = req.target_sites or ["Site A (Aggregator)", "Site B (Direct)", "Site C (Discount)"]
    result = await llm_service.orchestrate_multi_tab_swarm(
        goal=req.goal,
        target_sites=default_sites
    )
    return result
