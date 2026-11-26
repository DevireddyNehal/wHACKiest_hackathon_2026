"""
AuraOS - LLM Intelligence & Action Planning Service
Routes micro-DOM and multi-tab queries to live LLMs or smart deterministic fallbacks.
"""

import httpx
import logging
import re
import uuid
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

    async def orchestrate_multi_tab_swarm(
        self,
        goal: str,
        target_sites: list[str],
        listings: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        """
        Pillar 3 (SynapseWeb): Compare pasted listing text, or return a labeled sample.
        """
        if listings:
            return self._compare_user_listings(goal, listings)

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
            "comparison_source": "SAMPLE",
            "message": "Illustrative sample data only. No websites were opened or queried.",
        }

    def _compare_user_listings(self, goal: str, listings: list[str]) -> Dict[str, Any]:
        rows = [_parse_listing(text, index) for index, text in enumerate(listings, start=1)]
        amounts = [_first_amount(row["stated_price"]) for row in rows]
        if len(rows) > 1 and all(amount is not None for amount in amounts):
            best_index = min(range(len(amounts)), key=lambda index: amounts[index])
            rows[best_index]["is_best"] = True
            winner_name = rows[best_index]["platform"]
            winner_price = rows[best_index]["stated_price"]
            savings = "Lowest stated price in the pasted text. Fees the snippets omit can change the total."
        else:
            winner_name = "No single pick"
            winner_price = "Not comparable from these snippets"
            savings = "At least one snippet has no stated price, so none is marked lower."
        return {
            "swarm_id": f"swarm_{uuid.uuid4().hex[:8]}",
            "goal": goal,
            "status": "COMPLETED",
            "sites_scanned": [row["platform"] for row in rows],
            "winner": {
                "platform": winner_name,
                "final_price": winner_price,
                "savings": savings,
                "delivery_or_time": "Not taken from a live site",
                "baggage": "Included only when the pasted text mentions it",
                "direct_url": None,
            },
            "comparison_matrix": rows,
            "prefilled_cart_ready": False,
            "consent_shield_active": True,
            "execution_mode": "FROM_USER_TEXT",
            "comparison_source": "USER_TEXT",
            "message": "Compared only the snippets you pasted. No websites were opened or queried.",
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

_AMOUNT_RE = re.compile(r"(?:₹|Rs\.?|INR|\$)\s*[\d,]+(?:\.\d+)?", re.IGNORECASE)
_FEE_WORDS = ("convenience", "fee", "tax", "gst", "seat", "baggage", "insurance", "surcharge", "charge")
_GAP_CHECKS = (
    ("total", "grand", "payable", "checkout"),
    ("cancel",),
    ("baggage", "luggage"),
)
_GAP_LABELS = (
    "a final checkout total",
    "a cancellation policy",
    "baggage rules",
)


def _first_amount(text: str) -> Optional[float]:
    match = re.search(r"[\d,]+(?:\.\d+)?", text or "")
    if not match:
        return None
    return float(match.group(0).replace(",", ""))


def _parse_listing(text: str, index: int) -> Dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    label = lines[0][:80] if lines and len(lines[0]) <= 80 else f"Listing {index}"
    amounts = _AMOUNT_RE.findall(text)
    fee_amounts: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(word in lowered for word in _FEE_WORDS):
            fee_amounts.extend(_AMOUNT_RE.findall(line))
    lowered_text = text.lower()
    missing = [
        label_text
        for words, label_text in zip(_GAP_CHECKS, _GAP_LABELS)
        if not any(word in lowered_text for word in words)
    ]
    if not amounts:
        missing.insert(0, "any stated price")
    stated = amounts[0] if amounts else "No price written in this snippet"
    fees = ", ".join(dict.fromkeys(fee_amounts)) if fee_amounts else "No fee amount is written in this snippet"
    return {
        "platform": label,
        "stated_price": stated,
        "fees_mentioned": fees,
        "not_in_text": "; ".join(missing) if missing else "The snippet mentions a total, cancellation, and baggage.",
        "base": stated,
        "fees": fees,
        "total": stated if any(word in lowered_text for word in ("total", "grand", "payable", "checkout")) else "Not stated",
        "is_best": False,
    }


llm_service = LLMService()
