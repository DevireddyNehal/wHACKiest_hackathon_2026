# GazeVoice prototype

A no-build browser prototype for hands-free browsing using voice commands and a pointer-based gaze stand-in.

## Run

From `E:\appbescom`:

```powershell
Set-Location E:\appbescom\gazevoice
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8002
```

Open `http://127.0.0.1:8002/`.

Use Chrome or Edge for the browser Speech Recognition API. Camera access requires the browser to ask for permission and works on localhost or HTTPS. The camera is preview-only. Real eye tracking is not implemented: mouse/pointer movement and a 900 ms dwell simulate gaze.

The page uses a local Vosk speech model and a WebSocket audio pipeline. It includes a text-command fallback, quick command buttons, recognition status, and a recent-command history. Audio is processed on the local machine and is not sent to a cloud speech service.
