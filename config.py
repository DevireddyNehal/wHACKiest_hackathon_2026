"""
AuraOS - Backend Configuration & Settings
Handles environment variables with automatic fallback to intelligent mock modes
so the entire system runs out-of-the-box for judges and developers even without paid API keys.
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "AuraOS Backend"
    VERSION: str = "1.0.0"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # AI & LLM Providers (OpenAI, Gemini, Anthropic, or AWS Bedrock)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # ElevenLabs Conversational Voice API (Hackathon Sponsor)
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default Rachel voice

    # Notification Services (WhatsApp / Telegram / Twilio)
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    WHATSAPP_FROM_NUMBER: str = os.getenv("WHATSAPP_FROM_NUMBER", "whatsapp:+14155238886")
    DEFAULT_ALERT_PHONE: str = os.getenv("DEFAULT_ALERT_PHONE", "+919876543210")

    # Mock mode flag: automatically active if API keys are not supplied
    @property
    def is_mock_llm(self) -> bool:
        return not bool(self.OPENAI_API_KEY or self.GEMINI_API_KEY or self.ANTHROPIC_API_KEY)

    @property
    def is_mock_voice(self) -> bool:
        return not bool(self.ELEVENLABS_API_KEY)

    @property
    def is_mock_notification(self) -> bool:
        return not bool(self.TWILIO_ACCOUNT_SID and self.TWILIO_AUTH_TOKEN)

settings = Settings()
