"""
AuraOS - ElevenLabs Conversational Voice Service
Connects to ElevenLabs streaming audio WebSocket / REST APIs for sub-300ms vocal feedback.
"""

import httpx
import logging
from typing import Optional, Dict, Any
from backend.config import settings

logger = logging.getLogger("AuraOS.Voice")

class VoiceService:
    def __init__(self):
        self.is_mock = settings.is_mock_voice
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID
        logger.info(f"VoiceService initialized. Mock mode: {self.is_mock}")

    async def generate_speech_stream(self, text: str) -> Optional[bytes]:
        """
        Generates realistic voice audio from ElevenLabs for vocal confirmation or HUD readout.
        """
        if self.is_mock or not self.api_key:
            logger.info(f"[MOCK VOICE OUTPUT]: Speaking text -> '{text}'")
            return None

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",  # lowest latency model
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    return res.content
                logger.error(f"ElevenLabs error ({res.status_code}): {res.text}")
        except Exception as e:
            logger.error(f"ElevenLabs TTS exception: {e}")

        return None

voice_service = VoiceService()
