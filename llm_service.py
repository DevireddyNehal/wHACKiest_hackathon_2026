"""
AuraOS - LLM Intelligence & Action Planning Service
Routes micro-DOM and multi-tab queries to live LLMs or smart deterministic fallbacks.
"""

import httpx
import logging
import re
from html import unescape
from typing import Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger("AuraOS.LLM")

class LLMService:
    def __init__(self):
        self.is_mock = settings.is_mock_llm
        logger.info(f"LLMService initialized. Mock mode: {self.is_mock}")

    async def analyze_micro_dom(self, dom_snippet: str, user_prompt: str, context_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Pillar 1 (SmartPoint): Analyzes the tiny 2KB DOM snippet under the user's cursor
        to unmask hidden fees, detect dark patterns, or explain confusing terms.
        """
        if not self.is_mock and settings.OPENAI_API_KEY:
            return await self._call_openai_dom_analysis(dom_snippet, user_prompt, context_url)

        # High-Fidelity Realistic Mock Engine for Hackathon Demos
        result = self._mock_dom_analysis(dom_snippet, user_prompt, context_url)
        result["analysis_mode"] = "DEMO_MOCK"
        return result

    async def orchestrate_multi_tab_swarm(self, goal: str, target_sites: list[str]) -> Dict[str, Any]:
        """
        Pillar 3 (SynapseWeb): Decomposes high-level intent into multi-tab parallel tasks
        and synthesizes cross-site results into a single comparison card.
        """
        if not self.is_mock and settings.OPENAI_API_KEY:
            return await self._call_openai_swarm(goal, target_sites)

        return self._mock_swarm_results(goal, target_sites)

    def _mock_dom_analysis(self, dom_snippet: str, user_prompt: str, context_url: Optional[str] = None) -> Dict[str, Any]:
        prompt_lower = (user_prompt or "").lower()
        snippet_lower = (dom_snippet or "").lower()
        observed_text = unescape(re.sub(r"<[^>]*>", " ", dom_snippet or ""))
        observed_text = re.sub(r"\s+", " ", observed_text).strip()[:500]
        fee_terms = ("price", "fee", "cost", "fare", "convenience", "flight", "total")
        risk_terms = ("trap", "terms", "condition", "renew", "cancel", "legal", "clause")
        pricing_found = any(word in snippet_lower for word in fee_terms)
        terms_found = any(word in snippet_lower for word in risk_terms)

        if any(word in prompt_lower or word in snippet_lower for word in fee_terms):
            return {
                "category": "PRICING_UNMASKED",
                "title": "Pricing context highlighted" if pricing_found else "Pricing question · limited excerpt",
                "badge": "Demo analysis · verify the final total",
                "summary": (
                    "Fee or pricing language was found in the selected text. This small excerpt cannot verify a final checkout total or reveal charges that are not shown here."
                    if pricing_found
                    else "Your question asks about pricing, but this excerpt does not contain fee details. A final total cannot be verified from the text provided."
                ),
                "breakdown": [
                    {"item": "Selected text", "amount": observed_text or "No readable text supplied"},
                    {"item": "Final total", "amount": "Not verifiable from this excerpt", "warning": True},
                ],
                "action_recommendation": "Review the full checkout breakdown before making a decision.",
                "latency_ms": 42,
                "demo_mode": True,
            }

        if any(word in prompt_lower or word in snippet_lower for word in risk_terms):
            return {
                "category": "DARK_PATTERN_WARNING",
                "title": "Terms language highlighted" if terms_found else "Terms question · limited excerpt",
                "badge": "Demo analysis · review the full terms",
                "summary": (
                    "The selected excerpt mentions terms or cancellation. The prototype cannot determine whether a policy is unfair without the complete context."
                    if terms_found
                    else "Your question asks about terms, but this excerpt does not include policy details. The prototype cannot assess the full policy from this text."
                ),
                "breakdown": [
                    {"item": "Selected text", "amount": observed_text or "No readable text supplied"},
                    {"item": "Context", "amount": "Only the user-provided excerpt was analyzed"},
                ],
                "action_recommendation": "Check the complete policy and cancellation instructions.",
                "latency_ms": 42,
                "demo_mode": True,
            }

        return {
            "category": "EXECUTIVE_SUMMARY",
            "title": "Selected context summarized",
            "badge": "Demo analysis · user-provided text",
            "summary": "This local demo only analyzes the text included below; it does not inspect the rest of the page.",
            "breakdown": [
                {"item": "Selected text", "amount": observed_text or "No readable text supplied"},
                {"item": "Your request", "amount": (user_prompt or "Explain this")[:160]},
            ],
            "action_recommendation": "Share only the specific text you want help understanding.",
            "latency_ms": 42,
            "demo_mode": True,
        }

    def _mock_swarm_results(self, goal: str, target_sites: list[str]) -> Dict[str, Any]:
        return {
            "swarm_id": "swarm_94821a",
            "goal": goal or "Find best flight Bangalore to Delhi under ₹6,000",
            "status": "COMPLETED",
            "sites_scanned": target_sites or ["MakeMyTrip", "IndiGo Direct", "EaseMyTrip", "Skyscanner"],
            "winner": {
                "platform": "IndiGo Direct",
                "final_price": "₹4,800 (sample)",
                "savings": "Illustrative comparison only",
                "delivery_or_time": "Sample itinerary · not live",
                "baggage": "Sample baggage detail · verify with provider",
                "direct_url": None
            },
            "comparison_matrix": [
                {"platform": "IndiGo Direct", "base": "₹4,800", "fees": "₹0", "total": "₹4,800", "is_best": True},
                {"platform": "MakeMyTrip", "base": "₹4,899", "fees": "₹1,950", "total": "₹6,849", "is_best": False},
                {"platform": "EaseMyTrip", "base": "₹5,100", "fees": "₹650", "total": "₹5,750", "is_best": False}
            ],
            "prefilled_cart_ready": False,
            "consent_shield_active": True,
            "execution_mode": "SIMULATED",
            "message": "Illustrative sample data only. No websites were opened or queried.",
        }

    async def _call_openai_dom_analysis(self, dom_snippet: str, user_prompt: str, context_url: Optional[str]) -> Dict[str, Any]:
        # Live OpenAI integration if API key is provided
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "response_format": {"type": "json_object"},
                        "messages": [
                            {"role": "system", "content": "You are AuraOS SmartPoint engine. Analyze the provided DOM element and user prompt. Return JSON with title, badge, summary, breakdown (array of items with amount), and action_recommendation."},
                            {"role": "user", "content": f"URL: {context_url}\nPrompt: {user_prompt}\nDOM:\n{dom_snippet}"}
                        ]
                    }
                )
                if res.status_code == 200:
                    import json
                    data = res.json()
                    parsed = json.loads(data["choices"][0]["message"]["content"])
                    if not isinstance(parsed, dict):
                        raise ValueError("OpenAI response was not a JSON object.")
                    fallback = self._mock_dom_analysis(dom_snippet, user_prompt, context_url)
                    result = {**fallback, **parsed}
                    for field in ("title", "badge", "summary", "action_recommendation", "category"):
                        if not isinstance(result.get(field), str):
                            result[field] = fallback[field]
                        result[field] = result[field][:500]
                    rows = result.get("breakdown")
                    if not isinstance(rows, list):
                        rows = fallback["breakdown"]
                    result["breakdown"] = [
                        {
                            "item": str(row.get("item", "Detail"))[:100],
                            "amount": str(row.get("amount", "Not provided"))[:500],
                        }
                        for row in rows[:10]
                        if isinstance(row, dict)
                    ]
                    result["latency_ms"] = 320
                    result["analysis_mode"] = "OPENAI"
                    return result
        except Exception as e:
            logger.error(f"OpenAI call failed, falling back to mock: {e}")
        fallback = self._mock_dom_analysis(dom_snippet, user_prompt, context_url)
        fallback["analysis_mode"] = "DEMO_FALLBACK"
        return fallback

    async def _call_openai_swarm(self, goal: str, target_sites: list[str]) -> Dict[str, Any]:
        return self._mock_swarm_results(goal, target_sites)

llm_service = LLMService()
