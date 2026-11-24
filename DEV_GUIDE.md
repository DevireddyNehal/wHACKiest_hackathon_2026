# 🛠️ AuraOS Developer & AI Agent Execution Guide

> **Current implementation notice:** Some historical sections below describe planned capabilities, not shipped behavior. The runnable dashboard is the source of truth; see `README.md` for current demo limits. Do not describe the prototype as monitoring portals, bypassing queues, booking, or making payments.

---

## 🧭 Project Mental Model

AuraOS is a **wHACKiest 2026 (Track 02: Beyond the Browser) prototype** with five connected demo tools:
1. **SmartPoint:** User-submitted text analysis; the extension can send a small selected element on request.
2. **AirTouch:** Pointer-based laser, simulated pinch selection, and simulated scroll; no camera tracking.
3. **SynapseWeb:** Illustrative comparison data; no websites are queried.
4. **GhostButler:** In-memory reminder templates with an optional due time and a manually confirmed in-app alert preview only.
5. **RewindWeb:** Explicitly saved text notes and keyword search in process memory; no browser-history capture.

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
* **Verify:** Open `http://127.0.0.1:8000/` for the dashboard. `/api/status` reports backend mode and `/health` is the health check.
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
python tests/test_api.py
```
The tests cover the dashboard, bounded SmartPoint context, simulated Synapse results, GhostButler confirmation, and explicit RewindWeb capture.

---

## 🧪 How to Demo Each Pillar

### Demo 1: SmartPoint (Desk Mode)
1. Open a webpage in Chrome and deliberately hover over a small text element.
2. Use the extension shortcut or enter a text prompt in the side panel.
3. **Expected Result:** A HUD shows a demo explanation of the selected excerpt. It cannot verify charges or infer unseen page content.

### Demo 2: AirTouch (Air Mode)
1. In the SidePanel, click **Air Mode**.
2. **Expected Result:** Pointer movement projects a virtual laser. Hand tracking and camera use are not implemented.

### Demo 3: SynapseWeb Multi-Tab Swarm
1. In the SidePanel, open the SynapseWeb comparison card.
2. Click **Show sample comparison**.
3. **Expected Result:** A clearly labeled illustrative matrix appears. No sites are opened and no cart is prepared.

### Demo 4: GhostButler In-App Alert
1. In the dashboard or SidePanel, choose **Preview a demo alert**.
2. Confirm the browser confirmation dialog.
3. **Expected Result:** An in-app preview appears. No site is monitored, no booking is made, and no notification is sent externally.

### Demo 5: RewindWeb Text Search
1. In the SidePanel, look at the **RewindWeb Semantic Memory** card.
2. In the search box, type `LLM` or `hackathon`.
3. **Expected Result:** Matching sample notes appear. Save only text you choose; entries reset when the backend restarts.

---

## 🔑 Optional Provider Configuration

AuraOS runs with deterministic demo responses by default. An optional OpenAI key enables provider analysis for the text excerpt submitted to SmartPoint; the UI labels this and notes that the backend forwards that excerpt to OpenAI. Other listed service variables are scaffolding and are not used by the dashboard.

To enable OpenAI analysis, create a `.env` file in the root folder:
```env
# Submitted SmartPoint excerpts are sent to OpenAI
OPENAI_API_KEY="sk-..."
```

---

## 🚀 Safe Extension Principles

When extending the prototype, use official provider APIs and do not bypass site queues or access controls. Never book or initiate payment without a separate explicit user action. The deck and pitch script are concept drafts; verify every claim against the current implementation before presenting.
