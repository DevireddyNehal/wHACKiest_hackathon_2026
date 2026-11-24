# 📊 wHACKiest 2026 — Official PPT Deck Content
> **Track:** Track 02 — *Beyond the Browser*  
> **File Naming Format:** `TeamName_Track2.pptx` (Upload to Google Drive with permission "Anyone with link can view")  
> **Official Constraint:** Use the official template without adding extra slides. Paste the exact text below into each slide.

---

## 🟩 SLIDE 1: Cover Slide
* **Title:** AuraOS — The Autonomous Web Operating System
* **Subtitle:** Beyond the Browser: Reimagining how humans perceive, navigate, and delegate the web.
* **Track:** Track 02 — *Beyond the Browser*
* **Team Name:** [Your Team Name]
* **College:** Ramaiah Institute of Technology (MSRIT), Bengaluru
* **Team Members:** [Names & Year/Branch]

---

## 🟩 SLIDE 2: Problem Statement & Why Existing Tools Fail
* **The Core Crisis:**
  The World Wide Web was built 30 years ago as a static document reader. Today, humans use it as a complex transactional OS, forcing users to act as manual routers—juggling 15+ tabs, battling dark patterns, and doing endless cognitive grunt work.
* **Why Current Solutions Fail:**
  1. **Chatbots are Blind & Paralyzed:** ChatGPT/Claude answer text questions, but cannot see or act inside live, dynamic, authenticated web apps.
  2. **Traditional Screen Readers & Voice Tools are Clunky:** They read raw HTML linearly; asking a voice bot to navigate dynamic Single Page Apps (SPAs) results in severe latency (8–15s lag) and confusion.
  3. **The Babysitting Exhaustion:** Everyday people waste hours frantically refreshing crashing portals (Tatkal train slots at 10 AM, university exam results, flash sales).
  4. **Predatory Dark Patterns:** Aggregators and e-commerce platforms intentionally hide convenience fees and auto-renewal traps until the final payment step.

---

## 🟩 SLIDE 3: Proposed Solution — AuraOS (The 5 Pillars)
* **One-Sentence Vision:** AuraOS turns the browser from a passive viewing canvas into an active, multi-modal autonomous execution environment across Time, Space, and Autonomy.
* **The 5 Pillars:**
  1. **SmartPoint (Desk Mode):** Hover-to-act micro-comprehension. Analyzes only the 2KB micro-DOM under the cursor to unmask hidden checkout fees and legal traps in <150ms.
  2. **AirTouch (Air Mode):** Hands-free spatial computing via webcam (Google MediaPipe). Point a virtual laser with your finger, pinch to click, and wave to scroll.
  3. **SynapseWeb (Multi-Tab Swarm):** Deploys parallel browser workers across competitor sites, uncovering true final prices and presenting a unified 1-click comparison card.
  4. **GhostButler (The Asynchronous Future):** Background cloud daemon that monitors slots and queues 24/7 while your laptop is closed, dispatching WhatsApp alerts with 1-tap UPI payment links.
  5. **RewindWeb (Cognitive Memory):** Local-first semantic memory that lets you search concepts across past browsing history and visually roll back page states.

---

## 🟩 SLIDE 4: System Architecture & Technical Depth
* **Client-Side (Chrome Manifest V3):**
  - Content Scripts isolating micro-DOM bounding boxes to achieve 95% token reduction.
  - Google MediaPipe WebAssembly framework for 30 FPS hand landmark tracking and raycasting.
  - Frosted-glass floating popover HUD with zero layout shift.
* **Backend Orchestration (FastAPI & Serverless):**
  - High-concurrency async endpoints routing micro-DOM analysis and multi-tab swarms.
  - Asynchronous background scheduler for GhostButler portal monitoring.
* **Sponsor Technology Integration:**
  - **ElevenLabs (Hackathon Sponsor):** Integrated via low-latency Conversational Voice WebSockets (`/ws/voice`) for full-duplex spoken feedback and voice interruption.
  - **AWS (Hackathon Sponsor):** Scalable serverless execution on **AWS Lambda** for background workers, with LLM routing via **AWS Bedrock**.
  - **Twilio / Meta API:** WhatsApp webhook dispatcher for asynchronous mobile alerts.

---

## 🟩 SLIDE 5: Feasibility, Prototype Demo & Future Roadmap
* **What We Have Built (Current MVP):**
  - Fully functional Chrome Manifest V3 Extension with SidePanel Command Center.
  - Working SmartPoint engine that unmasks hidden fees and dark patterns in real-time.
  - Operational multi-tab comparison matrix generator.
  - Live GhostButler WhatsApp alert webhook dispatcher.
  - Verified test suite with 100% pass rate (`tests/test_api.py`).
* **Roadmap for 24-Hour Offline Hackathon (Dec 1–2):**
  - Direct integration with IRCTC / BookMyShow Tatkal session bypass.
  - Fully local vector embedding storage via IndexedDB for instant client-side Rewind memory.
  - Biometric passkey integration for seamless "Consent Shield" checkout authorization.
* **Target Audience & Impact:**
  - Everyday consumers (protecting against deceptive pricing).
  - Students & citizens (eliminating portal babysitting and bureaucracy).
  - Motor-disabled users (providing touch-free, hands-free web autonomy).
