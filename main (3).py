from pathlib import Path
import json
import io
import zipfile

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from vosk import KaldiRecognizer, Model


HERE = Path(__file__).resolve().parent
MODEL_DIR = HERE / "vosk-model-small-en-us-0.15"

app = FastAPI(title="GazeVoice Local Speech")
model = Model(str(MODEL_DIR)) if MODEL_DIR.is_dir() else None


@app.get("/")
def home():
    return FileResponse(HERE / "index.html")


@app.get("/api/speech-status")
def speech_status():
    return {
        "available": model is not None,
        "mode": "local-vosk" if model is not None else "unavailable",
        "model": MODEL_DIR.name if model is not None else None,
    }


@app.get("/download/source")
def download_source():
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in ("index.html", "main.py", "README.md"):
            path = HERE / name
            if path.is_file():
                bundle.write(path, f"gazevoice/{name}")
        requirements = HERE.parent / "requirements.txt"
        if requirements.is_file():
            bundle.write(requirements, "gazevoice/requirements.txt")
    archive.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="gazevoice-source.zip"'}
    return StreamingResponse(archive, media_type="application/zip", headers=headers)


@app.websocket("/ws/speech")
async def speech_socket(websocket: WebSocket):
    await websocket.accept()
    if model is None:
        await websocket.send_text(json.dumps({"error": "Local speech model not installed"}))
        await websocket.close()
        return

    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    try:
        while True:
            data = await websocket.receive_bytes()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text"):
                    await websocket.send_text(json.dumps({"final": result["text"]}))
            else:
                result = json.loads(recognizer.PartialResult())
                if result.get("partial"):
                    await websocket.send_text(json.dumps({"partial": result["partial"]}))
    except WebSocketDisconnect:
        pass
