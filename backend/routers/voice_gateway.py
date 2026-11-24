"""
AuraOS - Voice Gateway WebSocket
Enables full-duplex sub-300ms bidirectional speech streaming between browser extension & ElevenLabs.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging
from backend.services.llm_service import llm_service
from backend.services.voice_service import voice_service

router = APIRouter(prefix="/ws", tags=["VoiceGateway"])
logger = logging.getLogger("AuraOS.WebSocket")

@router.websocket("/voice")
async def voice_websocket_endpoint(websocket: WebSocket):
    """
    Sub-second bidirectional voice stream.
    Receives voice transcripts or raw audio chunks from Chrome extension sidepanel,
    processes DOM intent, and streams back voice responses.
    """
    await websocket.accept()
    logger.info("Voice WebSocket connection established with Chrome Extension")

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            event_type = data.get("type", "VOICE_COMMAND")

            if event_type == "VOICE_COMMAND":
                transcript = data.get("transcript", "")
                dom_context = data.get("dom_snippet", "")
                mode = data.get("mode", "DESK")  # DESK or AIR

                logger.info(f"Received speech in {mode} mode: '{transcript}'")

                # Analyze intent via LLM
                analysis = await llm_service.analyze_micro_dom(
                    dom_snippet=dom_context,
                    user_prompt=transcript
                )

                # Send structured response back to HUD
                await websocket.send_text(json.dumps({
                    "type": "HUD_RESPONSE",
                    "mode": mode,
                    "payload": analysis
                }))

            elif event_type == "PING":
                await websocket.send_text(json.dumps({"type": "PONG", "status": "CONNECTED"}))

    except WebSocketDisconnect:
        logger.info("Voice WebSocket disconnected cleanly")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
