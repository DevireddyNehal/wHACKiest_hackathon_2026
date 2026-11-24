"""
AuraOS - SmartPoint Router
Endpoint for micro-DOM analysis and instant contextual comprehension (<200ms).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from backend.services.llm_service import llm_service
from backend.services.voice_service import voice_service

router = APIRouter(prefix="/api/smartpoint", tags=["SmartPoint"])

class SmartPointRequest(BaseModel):
    dom_snippet: str = Field(min_length=1, max_length=2500)
    user_prompt: Optional[str] = Field(default="Explain this selected text", max_length=300)
    url: Optional[str] = Field(default=None, max_length=500)
    speak_response: Optional[bool] = False

    @field_validator("dom_snippet")
    @classmethod
    def require_nonblank_snippet(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Selected text cannot be blank.")
        return value

class SmartPointResponse(BaseModel):
    category: str
    title: str
    badge: str
    summary: str
    breakdown: list[Dict[str, Any]]
    action_recommendation: str
    latency_ms: int
    analysis_mode: str

@router.post("/analyze", response_model=SmartPointResponse)
async def analyze_element(req: SmartPointRequest):
    """
    Receives a tiny micro-DOM snippet extracted at the user's cursor or laser point.
    Returns structured analysis (unmasked fees, plain English explanation, trap warnings).
    """
    if not req.dom_snippet:
        raise HTTPException(status_code=400, detail="Missing dom_snippet")

    result = await llm_service.analyze_micro_dom(
        dom_snippet=req.dom_snippet,
        user_prompt=req.user_prompt or "Analyze this",
        context_url=req.url
    )

    # Optional vocalization using ElevenLabs
    if req.speak_response:
        speech_text = f"{result['title']}. {result['summary']}"
        await voice_service.generate_speech_stream(speech_text)

    return result
