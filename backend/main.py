"""
AuraOS - Master Backend Server Entrypoint
The Autonomous Web Operating System for wHACKiest 2026 (Track 02: Beyond the Browser)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import logging

from backend.config import settings
from backend.routers import smartpoint_api, synapse_swarm, ghost_butler, rewind_memory, voice_gateway

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AuraOS.Main")

app = FastAPI(
    title="AuraOS - The Autonomous Web Operating System",
    description="Local API for the AuraOS five-pillar prototype. External site automation, booking, messaging, and payments are not enabled.",
    version="1.0.0"
)
APP_ROOT = Path(__file__).resolve().parent.parent

# Enable CORS for Chrome Extension and local frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_origin_regex=r"chrome-extension://[a-p]{32}",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount 5 Pillar Routers
app.include_router(smartpoint_api.router)
app.include_router(synapse_swarm.router)
app.include_router(ghost_butler.router)
app.include_router(rewind_memory.router)
app.include_router(voice_gateway.router)

@app.get("/")
def root_status():
    return FileResponse(APP_ROOT / "index.html")

@app.get("/api/status")
def api_status():
    return {
        "project": "AuraOS",
        "tagline": "The Autonomous Web Operating System",
        "hackathon": "wHACKiest 2026 - CodeRIT MSRIT Bengaluru",
        "track": "Track 02: Beyond the Browser",
        "status": "ONLINE",
        "mock_mode": not bool(settings.OPENAI_API_KEY),
        "demo_mode": True,
        "analysis_mode": "OPENAI_CONFIGURED" if settings.OPENAI_API_KEY else "DEMO_MOCK",
        "pillars": {
            "pillar_1_smartpoint": "/api/smartpoint/analyze",
            "pillar_2_airtouch_voice": "/ws/voice",
            "pillar_3_synapse_swarm": "/api/swarm/execute",
            "pillar_4_ghost_butler": "/api/butler/missions",
            "pillar_5_rewind_memory": "/api/memory/search"
        },
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting AuraOS Backend on {settings.HOST}:{settings.PORT}")
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
