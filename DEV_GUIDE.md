# 🛠️ AuraOS Developer & AI Agent Execution Guide

> **NOTICE FOR DEVELOPERS & AI ASSISTANTS (Claude, Codex, Cursor, Gemini):**  
> Read this entire document before writing or editing code. This guide details the exact architecture, execution flow, testing procedures, and extension points for **AuraOS**.

---

## 🧭 Project Mental Model

AuraOS is an **Autonomous Web Operating System** designed for **wHACKiest 2026 (Track 02: Beyond the Browser)**.
It bridges 5 core pillars:
1. **SmartPoint (Desk Mode):** Cursor hover + `Alt+S` extracts a tiny micro-DOM under the mouse and shows a floating HUD unmasking fees/traps.
2. **AirTouch (Air Mode):** MediaPipe webcam hand gestures (virtual laser pointer + pinch-to-click + palm-swipe scroll).
3. **SynapseWeb (Swarm Engine):** Multi-tab parallel browser runner that compares competitor sites and exposes hidden fees.
4. **GhostButler (Asynchronous Cloud Daemon):** 24/7 background slot sniper (Tatkal/results) that sends a WhatsApp notification with a 1-tap UPI payment link.
5. **RewindWeb (Cognitive Memory):** Semantic search over past browsing history with visual time-travel.

---

## 📂 Exact File-by-File Breakdown

```
wHACKiest_2026_hackathon/
│
├── README.md                      # High-level overview & pitch
├── ARCHITECTURE.md                # System diagrams, data flows, algorithms
├── DEV_GUIDE.md                   # THIS FILE (Developer instructions)
├── SUBMISSION_DECK.md             # The 5-slide PPT deck content for wHACKiest
├── PITCH_VIDEO_SCRIPT.md          # 3-minute video pitch recording script
│
├── extension/                     # Chrome Extension (Manifest V3)
│   ├── manifest.json              # Declarations, permissions (activeTab, sidePanel, storage)
│   ├── background/
│   │   └── service_worker.js      # Relays messages between content script & FastAPI (:8000)
│   ├── content/
│   │   ├── content_script.js      # Bridges SidePanel commands to SmartPoint & AirTouch
│   │   ├── smartpoint.js          # Hover listener, micro-DOM extractor, frosted-glass HUD
│   │   ├── airtouch.js            # Virtual laser dot, pinch-click, palm-scroll
│   │   └── styles.css             # Frosted-glass HUD styles, glowing badges, laser dot
│   ├── sidepanel/
│   │   ├── sidepanel.html         # Command Center UI (Desk/Air toggle, Swarm, Butler, Memory)
│   │   ├── sidepanel.js           # Frontend interactivity & REST/WebSocket client
│   │   └── sidepanel.css          # Sleek modern dark-theme styles
│   └── icons/                     # Extension icons (icon16, icon48, icon128)
│
├── backend/                       # Python FastAPI Backend
│   ├── main.py                    # Server root, CORS setup, mounts routers
│   ├── config.py                  # Pydantic Settings & automatic Mock fallback flags
│   ├── requirements.txt           # Dependencies (fastapi, uvicorn, httpx, pydantic)
│   ├── routers/
│   │   ├── smartpoint_api.py      # POST /api/smartpoint/analyze
│   │   ├── synapse_swarm.py       # POST /api/swarm/execute
│   │   ├── ghost_butler.py        # GET/POST /api/butler/missions & trigger-demo
│   │   ├── rewind_memory.py       # POST /api/memory/search & history
│   │   └── voice_gateway.py       # WS /ws/voice (bidirectional speech stream)
│   └── services/
│       ├── llm_service.py         # LLM router (OpenAI/Gemini + realistic mock engine)
│       ├── voice_service.py       # ElevenLabs API integration + mock logger
│       └── notification.py        # WhatsApp/Twilio integration + mock logger
│
├── tests/
│   └── test_api.py                # Automated pytest/python suite testing all 5 pillars
└── legacy_prototype/              # Preserved original GazeVoice Vosk prototype
```

---

## ⚡ How to Run the Project (Step-by-Step)

### 1. Start the Backend Server (Terminal 1)
```bash
cd wHACKiest_2026_hackathon

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
* **Verify:** Open your browser at `http://127.0.0.1:8000/`. You should see `{"project": "AuraOS", "status": "ONLINE"}`.  
* **Interactive Docs:** Visit `http://127.0.0.1:8000/docs` to test all Swagger endpoints interactively.

### 2. Load the Extension into Google Chrome
1. In Chrome, visit `chrome://extensions/`.
2. Toggle on **Developer mode** in the top-right corner.
3. Click **Load unpacked** (top-left).
4. Select the `extension/` folder inside this repository.
5. You will see **AuraOS — Autonomous Web Operating System** loaded.
6. Click the Extension icon or the SidePanel button to open the **AuraOS Command Center**.

### 3. Run the Automated Test Suite (Terminal 2)
```bash
PYTHONPATH=. .venv/bin/python tests/test_api.py
```
*All 5 tests must print `✓ Passed` and exit with code 0.*

---

## 🧪 How to Demo Each Pillar

### Demo 1: SmartPoint (Desk Mode)
1. Open any webpage in Chrome (e.g. Wikipedia, Amazon, or a news site).
2. Hover your mouse over any price tag, button, or dense paragraph.
3. Press `Alt + S` (or click *Desk Mode* in the sidepanel).
4. **Expected Result:** A glowing frosted-glass HUD card appears directly beneath the cursor displaying the unmasked fee breakdown, trap warnings, and latency in ms. Press `Escape` or the close icon to dismiss.

### Demo 2: AirTouch (Air Mode)
1. In the SidePanel, click **Air Mode**.
2. **Expected Result:** A neon-cyan virtual laser dot appears on the webpage. Moving your mouse/hand projects the laser onto clickable cards.

### Demo 3: SynapseWeb Multi-Tab Swarm
1. In the SidePanel, navigate to the **SynapseWeb Multi-Tab Swarm** card.
2. Click **Execute Parallel Swarm**.
3. **Expected Result:** Button updates to *"Scanning 3 parallel sites..."* and returns a structured comparison matrix showing IndiGo Direct saving ₹2,049 with 1-click checkout ready.

### Demo 4: GhostButler WhatsApp Alert
1. In the SidePanel, look at the **GhostButler Background Sniper** card.
2. Click **Simulate Slot Trigger & WhatsApp**.
3. **Expected Result:** A WhatsApp bubble appears showing the simulated alert dispatched to `+919876543210` with the 4-minute holding countdown and payment link. (Check your backend terminal to see the live console dispatch log).

### Demo 5: RewindWeb Semantic Search
1. In the SidePanel, look at the **RewindWeb Semantic Memory** card.
2. In the search box, type `LLM` or `hackathon`.
3. **Expected Result:** Memory items update dynamically with relevant historical page cards and timestamps.

---

## 🔑 Environment Variables & Live API Configuration

AuraOS has **Zero-Config Mock Fallbacks**: it works 100% out-of-the-box for judges and grading even if no external keys are provided!

To enable **LIVE Cloud AI Providers**, create a `.env` file in the root folder:
```env
# Optional LLM API Key (OpenAI / Gemini / Anthropic)
OPENAI_API_KEY="sk-..."

# ElevenLabs Conversational Voice API (Hackathon Sponsor)
ELEVENLABS_API_KEY="your-elevenlabs-key"
ELEVENLABS_VOICE_ID="21m00Tcm4TlvDq8ikWAM"

# Twilio WhatsApp API (For live phone alerts)
TWILIO_ACCOUNT_SID="your-twilio-sid"
TWILIO_AUTH_TOKEN="your-twilio-token"
WHATSAPP_FROM_NUMBER="whatsapp:+14155238886"
DEFAULT_ALERT_PHONE="+919876543210"
```

---

## 🚀 Tasks for the Next Engineer / AI Assistant

If you are continuing work on this repository:
- [ ] **Task 1 (AirTouch MediaPipe Script):** In `extension/content/airtouch.js`, include the official MediaPipe Hands CDN script tag (`https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js`) to stream actual webcam video frames into `updateLaser(x, y)`.
- [ ] **Task 2 (Live ElevenLabs Stream):** In `backend/routers/voice_gateway.py`, attach an ElevenLabs bidirectional streaming WebSocket client using the `websockets` library.
- [ ] **Task 3 (Playwright Swarm Workers):** In `backend/routers/synapse_swarm.py`, install `playwright` (`playwright install chromium`) and write an async worker to launch 3 headless browser contexts in parallel.
- [ ] **Task 4 (Presentation Video):** Record the 3-minute video pitch following the exact script in `PITCH_VIDEO_SCRIPT.md`.
- [ ] **Task 5 (PPT Submission):** Paste the contents of `SUBMISSION_DECK.md` into the official wHACKiest PowerPoint template.
