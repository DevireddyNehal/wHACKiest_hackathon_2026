"""
AuraOS - Voice Gateway WebSocket
Enables full-duplex sub-300ms bidirectional speech streaming between browser extension & ElevenLabs.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging
import re
from typing import Any, Dict

from pydantic import BaseModel, Field, field_validator

from backend.services.llm_service import llm_service
from backend.services.voice_service import voice_service

router = APIRouter(prefix="/ws", tags=["VoiceGateway"])
command_router = APIRouter(prefix="/api/voice", tags=["Voice commands"])
logger = logging.getLogger("AuraOS.WebSocket")


class VoiceCommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=250)

    @field_validator("command")
    @classmethod
    def trim_command(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Enter a voice command.")
        return value


def interpret_command(command: str) -> Dict[str, Any]:
    text = re.sub(r"\s+", " ", command.lower()).strip()
    text = re.sub(r"[.!?,]+$", "", text)

    if text in {"help", "commands", "what can you do"}:
        return {
            "intent": "help",
            "action": {"type": "none"},
            "reply": (
                "Try opening a tool, running a sample comparison, analyzing the "
                "shown snippet, enabling the pointer demo, or searching saved notes."
            ),
        }

    search_match = re.fullmatch(
        r"(?:search|find|look up)\s+(?:(?:my|saved)\s+)?"
        r"(?:memory|notes)(?:\s+(?:for|about))?(?:\s+(.+))?",
        text,
    )
    if search_match:
        query = (search_match.group(1) or "").strip()
        return {
            "intent": "search_memory",
            "action": {"type": "search_memory", "screen": "rewind", "query": query},
            "reply": f"Searching your demo notes{f' for {query}' if query else ''}.",
        }

    if re.fullmatch(
        r"(?:run|start|execute|do)\s+(?:the\s+)?(?:sample\s+)?comparison"
        r"(?:\s+now)?|compare\s+(?:the\s+)?(?:sample\s+)?options",
        text,
    ):
        return {
            "intent": "run_comparison",
            "action": {"type": "run_comparison", "screen": "synapse"},
            "reply": "Running the illustrative comparison. Its data is simulated.",
        }

    if re.fullmatch(
        r"(?:analyze|analyse|explain|check)\s+(?:this\s+)?"
        r"(?:snippet|selected text|charges)",
        text,
    ):
        return {
            "intent": "analyze_snippet",
            "action": {"type": "analyze_snippet", "screen": "smartpoint"},
            "reply": "Analyzing only the text currently shown in SmartPoint.",
        }

    if re.fullmatch(
        r"(?:turn on|enable|start|activate)\s+(?:the\s+)?"
        r"(?:airtouch|air touch|air mode|pointer demo)(?: mode)?",
        text,
    ):
        return {
            "intent": "enable_pointer",
            "action": {"type": "enable_pointer", "screen": "airtouch"},
            "reply": "Opening AirTouch and enabling its pointer-only practice demo.",
        }

    if re.fullmatch(r"(?:scroll )?down", text):
        return {
            "intent": "scroll",
            "action": {"type": "scroll", "direction": "down"},
            "reply": "Scrolling down.",
        }
    if re.fullmatch(r"(?:scroll )?up", text):
        return {
            "intent": "scroll",
            "action": {"type": "scroll", "direction": "up"},
            "reply": "Scrolling up.",
        }
    if text in {"go to top", "scroll to top"}:
        return {
            "intent": "scroll",
            "action": {"type": "scroll", "direction": "top"},
            "reply": "Moving to the top of the page.",
        }

    if (
        re.search(r"\b(?:create|set up|add)\s+(?:a\s+)?reminder\b", text)
        or re.search(r"\b(?:preview|trigger|send)\s+(?:the\s+)?(?:demo\s+)?alert\b", text)
    ):
        return {
            "intent": "confirmation_required",
            "action": {"type": "confirmation_required", "screen": "butler"},
            "reply": (
                "Opening GhostButler. Review the reminder and use its confirmation "
                "button yourself; voice commands cannot trigger alerts."
            ),
        }

    open_match = re.fullmatch(
        r"(?:please\s+)?(?:open|go to|show|switch to|navigate to|take me to)\s+"
        r"(?:the\s+)?(.+?)(?:\s+(?:screen|page|tool))?",
        text,
    )
    if open_match:
        target = open_match.group(1).strip()
        aliases = {
            "overview": "home",
            "home": "home",
            "dashboard": "home",
            "smartpoint": "smartpoint",
            "smart point": "smartpoint",
            "desk mode": "smartpoint",
            "airtouch": "airtouch",
            "air touch": "airtouch",
            "air mode": "airtouch",
            "synapseweb": "synapse",
            "synapse web": "synapse",
            "synapse": "synapse",
            "swarm": "synapse",
            "ghostbutler": "butler",
            "ghost butler": "butler",
            "reminders": "butler",
            "reminder": "butler",
            "rewindweb": "rewind",
            "rewind web": "rewind",
            "rewind": "rewind",
            "memory": "rewind",
        }
        screen = aliases.get(target)
        if screen:
            label = {
                "home": "Overview",
                "smartpoint": "SmartPoint",
                "airtouch": "AirTouch",
                "synapse": "SynapseWeb",
                "butler": "GhostButler",
                "rewind": "RewindWeb",
            }[screen]
            return {
                "intent": "navigate",
                "action": {"type": "navigate", "screen": screen},
                "reply": f"Opening {label}.",
            }

    return {
        "intent": "unknown",
        "action": {"type": "none"},
        "reply": (
            "I didn’t recognize that command. Try “open SynapseWeb”, "
            "“run comparison”, or “search notes for hackathon”."
        ),
    }


@command_router.post("/command")
async def handle_voice_command(request: VoiceCommandRequest) -> Dict[str, Any]:
    """Turn a short transcript into a safe, allowlisted dashboard action."""
    return interpret_command(request.command)


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
