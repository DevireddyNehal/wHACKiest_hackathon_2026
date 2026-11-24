"""
AuraOS - SynapseWeb Multi-Tab Swarm Router
Endpoint for parallel multi-site web automation, comparison, and form pre-fill.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.services.llm_service import llm_service

router = APIRouter(prefix="/api/swarm", tags=["SynapseSwarm"])

class SwarmRequest(BaseModel):
    goal: str
    target_sites: Optional[List[str]] = None
    max_parallel_tabs: Optional[int] = 3

class SwarmResponse(BaseModel):
    swarm_id: str
    goal: str
    status: str
    sites_scanned: List[str]
    winner: Dict[str, Any]
    comparison_matrix: List[Dict[str, Any]]
    prefilled_cart_ready: bool
    consent_shield_active: bool

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
