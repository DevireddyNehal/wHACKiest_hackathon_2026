"""
AuraOS - Asynchronous Notification Service
Delivers GhostButler task completions directly to user's WhatsApp / Telegram with 1-click execution.
"""

import logging
from typing import Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger("AuraOS.Notification")

class NotificationService:
    def __init__(self):
        self.is_mock = settings.is_mock_notification

    async def send_whatsapp_alert(
        self,
        to_phone: str,
        title: str,
        message: str,
        action_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches a WhatsApp alert when a GhostButler background task is completed
        (e.g., Tatkal slot booked, price dropped, hall ticket available).
        """
        target = to_phone or settings.DEFAULT_ALERT_PHONE
        full_text = f"🤖 *AuraOS GhostButler Alert*\n\n📌 *{title}*\n{message}\n"
        if action_url:
            full_text += f"\n🔗 *Action Required (Holds for 4 mins):*\n{action_url}"

        if self.is_mock or not settings.TWILIO_ACCOUNT_SID:
            logger.info("=" * 60)
            logger.info(f"📲 [WHATSAPP DISPATCHED TO {target}]")
            logger.info(full_text)
            logger.info("=" * 60)
            return {
                "status": "SENT_MOCK",
                "recipient": target,
                "message": full_text,
                "delivered_at": "Just now",
                "channel": "WhatsApp"
            }

        # Real Twilio WhatsApp API implementation if credentials exist
        try:
            import httpx
            url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url,
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                    data={
                        "From": settings.WHATSAPP_FROM_NUMBER,
                        "To": f"whatsapp:{target}",
                        "Body": full_text
                    }
                )
                return {"status": "SENT_LIVE", "sid": resp.json().get("sid")}
        except Exception as e:
            logger.error(f"Failed to dispatch live WhatsApp message: {e}")
            return {"status": "FAILED", "error": str(e)}

notification_service = NotificationService()
