"""RewindWeb demo memory: small text records stored in process memory only."""

import datetime
import uuid
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/memory", tags=["RewindWeb"])

MEMORY_INDEX: List[Dict[str, Any]] = [
    {
        "id": "demo_01",
        "url": "https://github.com/vllm-project/vllm",
        "title": "vLLM and efficient LLM serving",
        "snippet": "Demo memory: PagedAttention, KV cache, and serving large language models.",
        "timestamp": "Example · 2 days ago",
        "category": "Sample research",
        "demo": True,
    },
    {
        "id": "demo_02",
        "url": "https://devnovate.co/event/whackiest",
        "title": "wHACKiest 2026 — Beyond the Browser",
        "snippet": "Demo memory: a hackathon track about browser agents, accessibility, and search.",
        "timestamp": "Example · today",
        "category": "Sample event",
        "demo": True,
    },
    {
        "id": "demo_03",
        "url": "https://arxiv.org/",
        "title": "Research notes on model architecture",
        "snippet": "Demo memory: compare attention mechanisms, model efficiency, and benchmarks.",
        "timestamp": "Example · yesterday",
        "category": "Sample research",
        "demo": True,
    },
]


class MemoryQueryRequest(BaseModel):
    query: str = Field(default="", max_length=200)


class MemoryCaptureRequest(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    url: str = Field(default="", max_length=500)
    snippet: str = Field(default="", max_length=1000)


@router.get("/history")
async def get_recent_history() -> List[Dict[str, Any]]:
    """Return small text-only records; this prototype does not store page snapshots."""
    return list(reversed(MEMORY_INDEX))


@router.post("/capture")
async def capture_memory(req: MemoryCaptureRequest) -> Dict[str, Any]:
    """Save only the title, optional URL, and short excerpt the user submits."""
    item = {
        "id": f"mem_{uuid.uuid4().hex[:8]}",
        "url": req.url.strip(),
        "title": req.title.strip(),
        "snippet": req.snippet.strip(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "category": "Saved by you",
        "demo": False,
    }
    if not item["title"]:
        raise HTTPException(status_code=422, detail="A title is required.")
    MEMORY_INDEX.append(item)
    del MEMORY_INDEX[:-100]
    return {"status": "SAVED_IN_MEMORY", "item": item}


@router.delete("/history")
async def clear_history() -> Dict[str, str]:
    """Clear the current process's memory, including the sample entries."""
    MEMORY_INDEX.clear()
    return {"status": "CLEARED"}


@router.post("/search")
async def search_memory(req: MemoryQueryRequest) -> Dict[str, Any]:
    """Demo text search; no external embedding service or personal browser history is used."""
    terms = [term for term in req.query.lower().split() if term]
    results = [
        item
        for item in reversed(MEMORY_INDEX)
        if all(
            term in " ".join(
                str(item.get(field, ""))
                for field in ("title", "snippet", "category", "url")
            ).lower()
            for term in terms
        )
    ]
    return {
        "query": req.query,
        "results_count": len(results),
        "results": results,
        "mode": "DEMO_TEXT_SEARCH",
    }
