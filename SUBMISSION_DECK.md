# 📊 OFFICIAL SLIDE DECK: `TeamName_Track2.pptx`
> **Hackathon:** wHACKiest 2026 | Ramaiah Institute of Technology (MSRIT), Bengaluru  
> **Track:** Track 02 — *Beyond the Browser*  
> **Project Name:** **AuraOS — The Autonomous Web Operating System**  
> **Repository:** https://github.com/DevireddyNehal/wHACKiest_hackathon_2026  
> **Live Interactive Demo:** https://whackiest-hackathon-2026.onrender.com  
> **Status:** All empirical claims sourced, architecture verified, transparent prototype status.

---

## 🟩 SLIDE 1: COVER & MISSION STATEMENT

* **Slide Number:** `01 / 06`
* **Slide Title:** **AuraOS**
* **Subtitle:** *The Autonomous Web Operating System: Unifying element inspection, multi-site comparison, and background alerts into one continuous workflow.*
* **Hackathon Track:** Track 02 — *Beyond the Browser* (Tags: `Browser Agents`, `Web Automation`, `Accessibility`, `Search`)
* **Team Details:**
  * **Team Name:** `[Insert Your Team Name, e.g. Team Aura]`
  * **Institution:** Department of Computer Science & Engineering, Ramaiah Institute of Technology, Bengaluru
  * **Team Members:** `[Member 1 (Lead), Member 2, Member 3, Member 4]`
  * **Live Repository:** `https://github.com/DevireddyNehal/wHACKiest_hackathon_2026`
  * **Live Web Demo:** `https://whackiest-hackathon-2026.onrender.com`
  * **Demo Video:** `[Link placeholder — unlisted YouTube video to be recorded and added]`
* **Visual Layout Suggestion for Canva/PPT:**
  * Dark minimalist theme (`#0B0F19` deep navy background, `#38BDF8` cyan laser highlights, `#818CF8` indigo badges).
  * Center: Clean AuraOS logo with glowing halo and a graphic showing a browser window dissolving into spatial nodes and mobile alerts.

---

## 🟩 SLIDE 2: THE PROBLEM STATEMENT: DECEPTION, CLUTTER & DIGITAL FATIGUE

* **Slide Number:** `02 / 06`
* **Slide Title:** **The Friction of the Modern Web: Cognitive Load, Deception, and Inefficiency**
* **Header Metric Callout (Evidence-Based KPI Cards):**
  * 🔴 **11.1% (1,254 sites)** of ~11,000 evaluated shopping websites feature deceptive **Dark Patterns**, with popular sites more likely to use them *(Mathur et al., ACM CSCW 2019)*.
  * 🔴 **Regulatory Action:** In November 2023, the Indian Ministry of Consumer Affairs (DoCA) formally issued Guidelines for Prevention and Regulation of Dark Patterns under the Consumer Protection Act, which address deceptive practices including drip pricing and hidden costs.
  * 🔴 **Multi-Tab Cognitive Fatigue:** Routine comparisons often require several open tabs and manual mental math to identify hidden add-ons.
  * 🔴 **High-Demand Workflows:** High-demand drops, such as railway Tatkal and exam results, often fill quickly, creating time pressure.
  * 🔴 **Agent Payload Overhead:** Full-page agents send large DOM or screenshot payloads to LLMs, increasing token cost and latency.

* **Detailed Problem Breakdown:**
  1. **Humans as Manual Data Routers (Tab Hell):**
     * The web was designed for reading hyperlinked documents, but users treat it as an operating system. Comparing travel options or products requires juggling tabs and mentally tracking hidden fees.
  2. **Predatory Drip Pricing & Dark Patterns:**
     * Illustrative example: A flight listed at ₹4,899 increases at the payment gateway due to undisclosed convenience fees, seat selection surcharges, and pre-checked insurance add-ons.
  3. **The Web Babysitting Burden (High-Demand Drops):**
     * Users must nervously refresh dynamic portals (train booking drops, college counseling results) because missing a brief window forfeits availability.
  4. **The "Blind & Paralyzed" AI Paradox:**
     * Traditional LLM chatbots remain trapped in isolated sidebar textboxes, unable to see or interact directly with Single Page Apps (SPAs) behind logins.

---

## 🟩 SLIDE 3: THE VISION: 5 PILLARS UNITING PAST, PRESENT, AND FUTURE

* **Slide Number:** `03 / 06`
* **Slide Title:** **The Vision: 5 Pillars Uniting Past, Present, and Future Web Workflows**
* **Vision Statement:** *AuraOS aims to decouple web data and execution from visual clutter, creating a unified operating layer across all browsing contexts:*

* **The 5 Pillars as a Unified System (Where the Architecture is Going):**
  1. **🖱️ SmartPoint *(The Present — Desk Mode):*** Instant micro-DOM inspection under the cursor on `Alt+S`, highlighting and unmasking fee breakdowns in a targeted HUD card without transmitting full pages.
  2. **🖐️ AirTouch *(The Present — Pointer Mode):*** Touch-free virtual pointer navigation directly on the page, with hands-free webcam gesture tracking planned for accessibility.
  3. **⚡ SynapseWeb *(The Swarm Engine):*** Multi-tab browser orchestrator designed to parallel-scan competitor checkouts, with a human Consent Shield halting before transactions.
  4. **🤖 GhostButler *(The Future — Cloud Delegation):*** Asynchronous background daemons that monitor portal availability shifts and send instant WhatsApp alerts with 1-tap action links.
  5. **🕰️ RewindWeb *(The Past — Memory Store):*** Client-side memory search planned to remember inspected elements, quotes, and session findings across past browsing.

---

## 🟩 SLIDE 4: THE PLAN: CONNECTED PIPELINE, ROADMAP & BUSINESS MODEL

* **Slide Number:** `04 / 06`
* **Slide Title:** **The Plan: Connected Pipeline, Roadmap & Business Viability**

* **The Connected Pipeline (How the Pillars Unify):**
  * **Inspection $\rightarrow$ Memory:** Elements analyzed by SmartPoint automatically index into RewindWeb memory for instant retrieval.
  * **Swarm $\rightarrow$ Cloud Butler:** Winning competitor options hand off directly into GhostButler price-watch missions with one click.
  * **Voice Gateway:** Text-command and WebSocket audio gateway (`/ws/voice`, `/api/voice/command`) configured for speech assistant navigation.

* **Phased Roadmap (Planned Milestones):**
  * **Phase 1 (Post-Hackathon — Next 30 Days):** Planned WebAssembly-compiled local vector storage (DuckDB-Wasm / IndexedDB); planned deep-linking from WhatsApp alerts to checkout.
  * **Phase 2 (Medium-Term — 6 Months):** Planned tremor filtering and eye-gaze calibration for motor accessibility; planned enterprise workflow API for legacy non-API portals.
  * **Phase 3 (Long-Term — 12 Months):** Privacy-preserving community dark pattern registries (design goal).

* **Proposed Business Model (Theoretical Proposals):**
  * **B2C Freemium:** Free core Chrome extension; optional Pro subscription (proposed at ₹299/month) to offset cloud compute for continuous monitoring daemons.
  * **B2B Workflow Automation:** Proposed usage-based API licensing for automating legacy administrative portals.
  * **Revenue Share:** Proposed opt-in revenue share on verified savings (business model proposal; not implemented).

---

## 🟩 SLIDE 5: WHAT'S BUILT TODAY (VERIFIABLE PROTOTYPE STATUS)

* **Slide Number:** `05 / 06`
* **Slide Title:** **What's Built Today: Verifiable Prototype Status & Smoke Tests**

* **What's Built Today (Verified in Code & Tests):**
  1. **Chrome MV3 Extension:** SmartPoint micro-DOM hover analysis and in-page HUD card.
  2. **Local DOM Extraction:** `smartpoint.js` prunes SVGs, scripts, styles, noscript, and iframes, truncating output to 2,500 characters before sending to backend.
  3. **Side Panel Command Center:** All five modules accessible in one interface (`sidepanel.html`).
  4. **FastAPI Cloud Backend:** Deployed live on Render (`https://whackiest-hackathon-2026.onrender.com`) serving REST API endpoints and the interactive web demo (`index.html`).
  5. **Two Cross-Pillar Handoffs:** SmartPoint inspections auto-index into RewindWeb, and Swarm winners hand off to GhostButler price-watch missions.

* **Not Yet Built:**
  * Webcam hand tracking (currently mouse-driven virtual pointer), live automated booking, and live WhatsApp sending (currently simulated/logged).

* **Raw Verification Output (`tests/test_api.py`):**
  ```text
  PASS test_dashboard_and_health
  PASS test_smartpoint_uses_only_submitted_context
  PASS test_synapse_is_explicitly_simulated
  PASS test_voice_commands_are_bounded_and_allowlisted
  PASS test_ghostbutler_requires_confirmation_and_never_books
  PASS test_rewind_has_empty_state_and_explicit_capture
  PASS test_cross_pillar_handoffs

  Ran 7 tests in 0.11s. All checks passed.
  Note: AirTouch (Pillar 2) tested manually via browser DOM events; no automated backend test yet.
  ```

---

## 🟩 SLIDE 6: THE ASK & IMMEDIATE NEXT STEPS

* **Slide Number:** `06 / 06`
* **Slide Title:** **The Ask & Immediate Next Steps**

* **The Specific Ask:**
  * **Technical Feedback:** Mentorship and architectural feedback on our cross-pillar agent orchestration and lightweight micro-DOM pruning.
  * **Pilot Introductions:** Introductions to browser-agent engineering teams and accessibility researchers interested in evaluating our element-level inspection approach.

* **Immediate Next Steps:**
  1. **Offline Memory Engine:** Integrate WebAssembly-compiled local vector storage (DuckDB-Wasm) to eliminate backend dependencies for RewindWeb search.
  2. **Camera Gesture Tracking:** Integrate Google MediaPipe Hands WebAssembly into `airtouch.js` to transition the pointer from mouse-driven to true webcam gesture control.
  3. **Production Cloud Infrastructure:** Deploy backend daemons to AWS App Runner / AWS Lambda with ElevenLabs speech gateway integration.

---

### 💡 Quick Tip for Your Friend Making the PPT:
* Open PowerPoint, Google Slides, or Canva.
* Create a **6-slide deck**.
* Copy the exact text from **SLIDE 1 through SLIDE 6** into each respective slide.
* Save the file as **`TeamName_Track2.pptx`**, upload it to Google Drive, set the share permission to **"Anyone with the link can view"**, and submit the link on Devnovate!
