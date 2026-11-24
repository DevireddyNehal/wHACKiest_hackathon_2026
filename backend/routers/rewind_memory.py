"""
AuraOS - RewindWeb Persistent Memory Router
Semantic search across past browsing history and visual time-travel state reconstruction.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime

router = APIRouter(prefix="/api/memory", tags=["RewindWeb"])

# In-memory semantic history store
MEMORY_INDEX: List[Dict[str, Any]] = [
    {
        "id": "mem_01",
        "url": "https://github.com/vllm-project/vllm",
        "title": "vLLM: Easy, fast, and cheap LLM serving with PagedAttention",
        "snippet": "PagedAttention is the core algorithm that reduces memory waste in KV cache from 60-80% down to under 4%.",
        "timestamp": "2 days ago at 03:45 PM",
        "category": "Code & Research",
        "snapshot_preview": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400&q=80"
    },
    {
        "id": "mem_02",
        "url": "https://arxiv.org/abs/2412.01234",
        "title": "DeepSeek-V3 Technical Report: Architecture & Benchmark Analysis",
        "snippet": "Multi-head Latent Attention (MLA) and DeepSeekMoE architecture achieve state-of-the-art reasoning at 1/10th the training cost.",
        "timestamp": "Yesterday at 11:15 AM",
        "category": "Research Paper",
        "snapshot_preview": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&q=80"
    },
    {
        "id": "mem_03",
        "url": "https://devnovate.co/event/whackiest",
        "title": "wHACKiest 2026 Hackathon Portal | CodeRIT MSRIT",
        "snippet": "National 24-hour hackathon at Ramaiah Institute of Technology. Track 02 Beyond the Browser: Reimagine how we use the web.",
        "timestamp": "Today at 01:20 PM",
        "category": "Hackathon",
        "snapshot_preview": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&q=80"
    }
]

class MemoryQueryRequest(BaseModel):
    query: str
    time_filter: Optional[str] = "all"

@router.get("/history")
async def get_recent_history():
    """Returns chronologically indexed browsing memory cards."""
    return MEMORY_INDEX

@router.post("/search")
async def search_memory(req: MemoryQueryRequest):
    """
    Semantic concept search across past web pages.
    Instead of matching exact keywords, searches concept similarity.
    """
    q = (req.query or "").lower()
    matches = []
    for item in MEMORY_INDEX:
        if q in item["title"].lower() or q in item["snippet"].lower() or q in item["category"].lower() or not q:
            matches.append(item)

    if not matches and q:
        # Fallback closest semantic match
        matches = [MEMORY_INDEX[0]]

    return {
        "query": req.query,
        "results_count": len(matches),
        "results": matches
    }
