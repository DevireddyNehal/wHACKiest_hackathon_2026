# 🌐 AuraOS — The Autonomous Web Operating System
> **wHACKiest 2026** | **Track 02: Beyond the Browser**  
> *Department of Computer Science & Engineering, Ramaiah Institute of Technology (MSRIT), Bengaluru*

---

## 📌 The Problem: The 30-Year-Old Web is Broken

The World Wide Web was built in 1993 for hyperlinked document reading. Today, we use it as an interactive operating system for commerce, travel, research, work, and bureaucracy. This mismatch creates massive daily friction:

1. **Humans as Manual Data Routers:** Completing everyday tasks (booking flights, comparing medicine, checking exam results) forces users to juggle 15–20 open tabs, copy-paste data, and do exhausting cognitive grunt work.
2. **Predatory Dark Patterns & Hidden Fees:** Deceptive checkout countdowns, hidden convenience fees, and auto-renewing subscriptions trick everyday users.
3. **The Babysitting Nightmare:** Millions of students and citizens spend hours frantically refreshing crashing servers at 9:59 AM (Tatkal train slots, exam hall tickets, concert drops, doctor appointments).
4. **Current AI is Blind & Paralyzed:** Chatbots sit in isolated text boxes; they cannot interact with live, dynamic, authenticated web apps.

---

## 🚀 The Solution: AuraOS

**AuraOS** is the first **Autonomous Web Operating System** that bridges the **Past, the Present, and the Future** of your web experience. It turns the browser from a passive viewing canvas into an active, multi-modal autonomous execution environment.

```
                       ┌────────────────────────────────────────────────────────┐
                       │                       AURA OS                          │
                       │           (The Autonomous Web Operating System)        │
                       └───────────────────────────┬────────────────────────────┘
                                                   │
         ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
         ▼                                         ▼                                         ▼
   1. THE PRESENT                            2. THE FUTURE                             3. THE PAST
 (Real-Time Browsing)                    (Asynchronous Delegation)                 (Cognitive Memory)
         │                                         │                                         │
 ┌───────┴───────┐                         ┌───────┴───────┐                         ┌───────┴───────┐
 │  SMARTPOINT   │ Hover-to-Act /          │  GHOSTBUTLER  │ Background workers      │   REWINDWEB   │ Vector memory 
 │  (Desk Mode)  │ Micro-Comprehension     │               │ snipe queues & send     │               │ & time-travel 
 ├───────────────┤                         │               │ WhatsApp alerts         │               │ slider        
 │   AIRTOUCH    │ Hands-Free Spatial      └───────────────┘                         └───────────────┘
 │  (Air Mode)   │ Gestures via Webcam                                                       ▲
 ├───────────────┤                                                                           │
 │  SYNAPSEWEB   │ Multi-Tab Swarm                                                           │
 │  (The Brain)  │ Parallel Execution                                                        │
 └───────┬───────┘                                                                           │
         │                                                                                   │
         └───────────────────────────────── Feeds into Memory ───────────────────────────────┘
```

---

## 🏛️ The 5 Pillars of AuraOS

### 1. 🖱️ SmartPoint *(Desk Mode — Micro-Comprehension)*
* **What it does:** Effortlessly glide your cursor over *any* confusing web component (a 50-line legal clause, a hidden flight fee, a complex chart, or an error code) and press `Alt+S`.
* **The Magic:** Instead of dumping a 400KB webpage into an LLM, it extracts only the **2KB micro-DOM under your cursor**, unmasking hidden fees, flagging traps, or explaining concepts in **under 150ms**.

### 2. 🖐️ AirTouch *(Air Mode — Spatial Hands-Free Interaction)*
* **What it does:** Replaces finicky eye-tracking with rock-solid **Google MediaPipe Hand Gestures + ElevenLabs Conversational Voice**.
* **The Magic:** Sit back hands-free. Point your index finger to cast a glowing virtual laser onto any element, speak your intent (*"Summarize this"*, *"Buy this"*), pinch fingers to click, or swipe your palm to scroll smoothly.

### 3. ⚡ SynapseWeb *(The Multi-Tab Swarm Engine)*
* **What it does:** When a task requires comparing multiple sites (e.g., finding the cheapest direct flight or urgent medicine delivery), it opens and orchestrates 3–4 tabs in parallel.
* **The Magic:** Navigates past deceptive aggregator markups down to the real checkout screen, unmasks hidden convenience fees, and surfaces a single unified comparison card with 1-click execution.

### 4. 🤖 GhostButler *(The Asynchronous Future)*
* **What it does:** Solves the agony of babysitting tabs. GhostButler works 24/7 in the cloud **while your laptop is closed or asleep**.
* **The Magic:** Monitors dynamic portals, snipes high-demand slots (IRCTC Tatkal train tickets at 10 AM, university exam results, flash sales), pre-reserves the slot, and dispatches a **WhatsApp notification with a 1-tap UPI payment link** holding your spot.

### 5. 🕰️ RewindWeb *(The Cognitive Memory)*
* **What it does:** A privacy-first local semantic memory engine.
* **The Magic:** Instead of useless URL-only history, search concepts (*"What was that research paper on LLM memory I read on Tuesday?"*), or drag an interactive **Time-Travel Slider** to restore page states or accidentally closed forms.

---

## 🏆 Hackathon Alignment & Sponsor Technology

* **Official Track:** Track 02: *Beyond the Browser* (`Browser agents`, `Web automation`, `Accessibility`, `Search`).
* **ElevenLabs (Sponsor Prize):** Integrated via low-latency Conversational Voice WebSockets (`/ws/voice`) for full-duplex speech feedback and real-time audio interruptions.
* **AWS (Sponsor Prize):** Headless background workers and GhostButler daemons designed for serverless execution on **AWS Lambda** and **AWS ECS/App Runner**, with LLM routing via **AWS Bedrock**.

---

## ⚡ Quickstart Guide (Run in 2 Minutes)

### 1. Start the Backend Server
```bash
# Clone the repository
git clone <repo_url>
cd wHACKiest_2026_hackathon

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the master FastAPI orchestrator
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend is now live at `http://127.0.0.1:8000` (API Docs at `http://127.0.0.1:8000/docs`).*

### 2. Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in top-right corner).
3. Click **Load unpacked**.
4. Select the `extension/` folder inside this repository.
5. Click the AuraOS extension icon or side-panel to open the **AuraOS Command Center**!

### 3. Run the End-to-End Test Suite
```bash
PYTHONPATH=. python tests/test_api.py
```

---

## 📁 Repository Structure
```
wHACKiest_2026_hackathon/
├── README.md               # Master Project Overview
├── ARCHITECTURE.md         # Deep Technical Specifications & Data Flow
├── DEV_GUIDE.md            # Complete Step-by-Step Guide for Team & AI
├── SUBMISSION_DECK.md      # Exact Slide-by-Slide Content for PPT Template
├── PITCH_VIDEO_SCRIPT.md   # Word-for-Word 3-Minute Video Pitch Script
│
├── extension/              # Chrome Extension (Manifest V3)
│   ├── manifest.json       # MV3 Permissions & Declarations
│   ├── background/         # Service Worker & Message Router
│   ├── content/            # SmartPoint & AirTouch Content Scripts
│   ├── sidepanel/          # Command Center HTML/JS/CSS
│   └── icons/              # Extension Brand Icons
│
├── backend/                # Python FastAPI Master Orchestrator
│   ├── main.py             # Server Entrypoint
│   ├── config.py           # Settings & Mock Fallback Controls
│   ├── routers/            # 5-Pillar API Endpoints & WebSockets
│   └── services/           # LLM, ElevenLabs Voice & WhatsApp Services
│
└── tests/
    └── test_api.py         # Full 5-Pillar Automated Test Suite
```

---

## 👥 The Team — CodeRIT wHACKiest 2026
* Built with passion for **wHACKiest 2026**, Ramaiah Institute of Technology, Bengaluru.
* **Track:** 02 — *Beyond the Browser*
