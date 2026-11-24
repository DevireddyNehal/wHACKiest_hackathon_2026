# 🌐 AuraOS — A Browser Assistant Prototype
> **wHACKiest 2026** | **Track 02: Beyond the Browser**  
> *Department of Computer Science & Engineering, Ramaiah Institute of Technology (MSRIT), Bengaluru*

---

> **Current build:** This is a runnable demo, not an autonomous booking product. The dashboard uses simulated comparisons, an in-app-only reminder alert, pointer-based AirTouch controls, and text-only in-memory notes. It does not bypass queues, monitor sites, book slots, send WhatsApp messages, or initiate payment.

## 📌 The Problem: The 30-Year-Old Web is Broken

The World Wide Web was built in 1993 for hyperlinked document reading. Today, we use it as an interactive operating system for commerce, travel, research, work, and bureaucracy. This mismatch creates massive daily friction:

1. **Humans as Manual Data Routers:** Completing everyday tasks (booking flights, comparing medicine, checking exam results) forces users to juggle 15–20 open tabs, copy-paste data, and do exhausting cognitive grunt work.
2. **Predatory Dark Patterns & Hidden Fees:** Deceptive checkout countdowns, hidden convenience fees, and auto-renewing subscriptions trick everyday users.
3. **The Babysitting Nightmare:** Millions of students and citizens spend hours frantically refreshing crashing servers at 9:59 AM (Tatkal train slots, exam hall tickets, concert drops, doctor appointments).
4. **Current AI is Blind & Paralyzed:** Chatbots sit in isolated text boxes; they cannot interact with live, dynamic, authenticated web apps.

---

## 🚀 The Solution: AuraOS

**AuraOS** is an experimental browser-assistant prototype that explores how small, user-controlled tools could bring context, comparison, reminders, and memory closer to everyday browsing.

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
 │  (Desk Mode)  │ Micro-Comprehension      │               │ show local demo alerts  │               │ & text timeline
 ├───────────────┤                         │               │ local alert preview     │               │ slider
 │   AIRTOUCH    │ Hands-Free Spatial      └───────────────┘                         └───────────────┘
 │  (Air Mode)   │ Gestures via Webcam                                                       ▲
 ├───────────────┤                                                                           │
 │  SYNAPSEWEB   │ Multi-Tab Swarm                                                           │
 │  (The Brain)  │ Sample Comparison                                                        │
 └───────┬───────┘                                                                           │
         │                                                                                   │
         └───────────────────────────────── Feeds into Memory ───────────────────────────────┘
```

---

## 🏛️ The 5 Pillars of AuraOS

### 1. 🖱️ SmartPoint *(Desk Mode — Micro-Comprehension)*
* **Prototype:** Submit a short, user-selected text excerpt and a question. The local demo returns a bounded explanation and flags when the excerpt is too limited to verify a price or policy.
* **Limit:** This dashboard does not capture page content automatically; configured AI providers may receive the excerpt sent to the backend.

### 2. 🖐️ AirTouch *(Air Mode — Spatial Hands-Free Interaction)*
* **Prototype:** The dashboard demonstrates a virtual pointer and simulated pinch/scroll controls using mouse input.
* **Voice agent:** Use the dashboard microphone or typed command bar to navigate tools, run the sample comparison, analyze the shown SmartPoint excerpt, enable AirTouch, search notes, or scroll.
* **Limit:** Webcam hand tracking is not implemented; voice recognition depends on browser support and permission. The page does not request camera access.

### 3. ⚡ SynapseWeb *(The Multi-Tab Swarm Engine)*
* **Prototype:** Returns an illustrative comparison matrix to demonstrate how multi-site results could be presented.
* **Limit:** No sites are opened or queried, sample prices are fictional, and there is no cart or checkout action.

### 4. 🤖 GhostButler *(The Asynchronous Future)*
* **Prototype:** Saves an in-memory reminder template, optionally checks a scheduled time, and shows an in-app alert preview after explicit confirmation.
* **Limit:** There is no background scheduler, portal monitoring, queue bypass, booking, WhatsApp dispatch, or payment initiation.

### 5. 🕰️ RewindWeb *(The Cognitive Memory)*
* **Prototype:** Search example notes and save text, a title, and an optional URL only when you choose. A slider browses the visible text records.
* **Limit:** Search is keyword matching, entries are held in memory until the backend restarts, and no page snapshots or browser history are collected.

---

## 🏆 Hackathon Alignment & Sponsor Technology

* **Official Track:** Track 02: *Beyond the Browser* (`Browser agents`, `Web automation`, `Accessibility`, `Search`).
* The repository includes integration scaffolding, but this dashboard runs in demo mode and does not require sponsor credentials or external services.

---

## ⚡ Quickstart Guide

### 1. Start the Backend Server
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the API and dashboard
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Open the AuraOS dashboard at `http://127.0.0.1:8000`. API status is at `/api/status`; interactive API docs are at `/docs`.*
Choose a pillar card or sidebar item to open its own screen; use **Overview** to return to the menu.

The dashboard works without the Chrome extension. Loading `extension/` in Chrome is optional; extension features may require separate setup.

### Voice commands

On the dashboard, click **Start listening** and say one short command, or type the same command and choose **Run command**. Try “open SmartPoint”, “run comparison”, “analyze this snippet”, “turn on AirTouch”, “search notes for hackathon”, or “scroll down”. Chrome/Edge speech recognition requires microphone permission and a secure page (HTTPS or localhost); if recognition is unavailable, the typed command bar still works.

Recognition is one command at a time. The browser may process microphone audio through its speech provider; only the recognized words are sent to AuraOS. Command handling uses a small allowlist, and voice cannot trigger reminder alerts, bookings, payments, or messages. Spoken replies can be turned off in the dashboard.

### Publish a shareable demo with Render

The repository includes a Render Blueprint in `render.yaml` for deploying the dashboard and FastAPI backend together. Keep the GitHub repository private and grant Render access to it:

1. Push the deployment config and app changes to the GitHub `main` branch.
2. In Render, choose **New → Blueprint**, connect the private GitHub repository, and select `main`.
3. Review the `auraos-demo` web service and deploy it. Render will provide a public `onrender.com` URL to share.

The service uses demo/mock integrations and requires no API keys. The free instance may sleep when idle, so the first visit after inactivity can take longer. Reminder templates and saved notes are in-memory demo data and may be cleared when the service restarts.

### 2. Load the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in top-right corner).
3. Click **Load unpacked**.
4. Select the `extension/` folder inside this repository.
5. Click the AuraOS extension icon or side-panel to open the **AuraOS Command Center**!

## 🎬 Demo walkthrough

From the Overview, click a pillar card to open its own screen. Each screen includes its own quick-demo steps.

1. **SmartPoint:** Edit the sample excerpt or question, then click **Analyze this snippet**. The result only uses that excerpt. In Chrome, hover over a small element and press `Alt+S` to open the extension HUD.
2. **Voice agent / AirTouch:** Click **Start listening** and say “turn on AirTouch” or “open SynapseWeb”. You can also type the same commands if speech recognition is unavailable. Enable the pointer demo, aim at a practice tile, then simulate a pinch; no camera or hand tracking is used.
3. **SynapseWeb:** Enter a comparison goal and click **Run sample comparison**. Results are illustrative; no sites are queried and no cart is prepared.
4. **GhostButler:** Create a reminder template with an optional scheduled time. At or after that time, choose **Preview alert** and confirm. This creates an in-app preview only.
5. **RewindWeb:** Search `LLM` or `hackathon`, save an optional text note, and use the slider to select a record. Search is keyword-based and memory resets when the backend restarts.

### 3. Run the API smoke tests
```bash
python tests/test_api.py
```

---

## 📁 Repository Structure
```
wHACKiest_2026_hackathon/
├── README.md               # Master Project Overview
├── index.html              # Responsive dashboard served by FastAPI
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
# wHACKiest_hackathon_2026
