# 📊 wHACKiest 2026 — Verified Slide Deck (`TeamName_Track2.pptx`)
> **Track:** Track 02 — *Beyond the Browser*  
> **Repository:** https://github.com/DevireddyNehal/wHACKiest_hackathon_2026  
> **Note:** Every claim in this deck is verified, transparently labeled, and aligned with the actual repository implementation.

---

## 🟩 SLIDE 1: COVER & MISSION STATEMENT

* **Slide Number:** `01 / 06`
* **Title:** **AuraOS**
* **Subtitle:** *The Autonomous Web Operating System: Reimagining how humans perceive, navigate, and delegate web workflows.*
* **Track:** Track 02 — *Beyond the Browser* (Tags: `Browser Agents` · `Web Automation` · `Accessibility` · `Search`)
* **Team Details:**
  * **Team Name:** `[Your Team Name]`
  * **Institution:** Department of Computer Science & Engineering, Ramaiah Institute of Technology, Bengaluru
  * **Team Members:** `[Names & Branches/Years]`
  * **GitHub Repository:** `https://github.com/DevireddyNehal/wHACKiest_hackathon_2026`

---

## 🟩 SLIDE 2: THE PROBLEM: FRAGMENTATION, DECEPTION & DIGITAL FATIGUE

* **Slide Number:** `02 / 06`
* **Title:** **The Friction of the Modern Web: Cognitive Load, Deception, and Inefficiency**

* **Documented Evidence & Regulatory Context:**
  * 📌 **Prevalence of Dark Patterns:** In an empirical study of ~11,000 shopping websites, **11.1% (1,254 sites)** deployed deceptive dark patterns across 1,818 instances, with more popular shopping sites found to be more likely to feature them *(Mathur et al., ACM CSCW 2019)*.
  * 📌 **Regulatory Recognition:** In November 2023, the Indian Ministry of Consumer Affairs (DoCA) formally notified guidelines prohibiting 13 specific dark patterns under the Consumer Protection Act, explicitly including drip pricing, hidden costs, and disguised advertisements.
  * 📌 **High-Demand Portal Contention:** High-demand drop workflows (such as IRCTC Tatkal ticket openings, entrance exam results, and flash sales) frequently exhaust limited inventory within minutes, leaving everyday users vulnerable to slight network delays, server slowdowns, or input errors.
  * 📌 **Architectural Overhead in Web Agents:** Traditional visual browser agents process full-page screenshots or raw 300–400KB DOM dumps, which substantially increases token consumption and latency compared to focused, localized element extraction.

* **The Core Structural Problems:**
  1. **Manual Data Routing:** Routine research (comparing travel, sourcing hardware, evaluating services) forces users to keep 10–15 tabs open simultaneously and manually extract and compare numbers across fragmented layouts.
  2. **Drip Pricing & Hidden Friction:** Displayed prices routinely omit mandatory convenience fees, baggage rules, or auto-renewal terms until the final checkout screen.
  3. **The Babysitting Burden:** Users are forced to actively wait on and refresh dynamic portals instead of delegating the wait to an automated assistant.
  4. **Accessibility Barriers:** Complex, ad-heavy web applications remain high-friction for users with motor tremors, repetitive strain injuries (RSI), or temporary physical limitations.

---

## 🟩 SLIDE 3: THE SOLUTION — AURAOS (THE 5-PILLAR ARCHITECTURE)

* **Slide Number:** `03 / 06`
* **Title:** **AuraOS: A Unified Architecture Across Time, Space, and Autonomy**
* **Core Idea:** *AuraOS decouples web intent and execution from the visual noise of websites, providing tools for immediate inspection, hands-free interaction, and asynchronous delegation.*

* **The 5 Pillars & Realistic Implementation Status:**
  1. **🖱️ SmartPoint *(Desk Mode — Micro-Comprehension)* [Functional Prototype]**
     * Hover mouse over any webpage element and press `Alt+S`.
     * Extracts only the targeted **2KB micro-DOM bounding box**, identifying hidden convenience fees, auto-renewal terms, or complex text in an in-place frosted-glass HUD.
  2. **🖐️ AirTouch *(Air Mode — Hands-Free Interaction)* [Experimental Prototype]**
     * Integrates **Google MediaPipe Hands** via standard laptop webcam.
     * Projects a virtual laser pointer from the index finger with pinch-to-click and palm-scroll handlers for touch-free accessibility.
  3. **⚡ SynapseWeb *(Multi-Tab Execution)* [Prototype Orchestrator]**
     * Backend orchestrator that models parallel execution across competitor sites (e.g., direct carrier vs. aggregator).
     * Synthesizes cross-site data into a single comparison card with an explicit **Consent Shield** halting before payments.
  4. **🤖 GhostButler *(Asynchronous Delegation)* [Architecture & Notification Prototype]**
     * Asynchronous background daemon tracking portal availability and dispatching **WhatsApp alerts with 1-tap checkout links**.
     * *Compliance Boundary:* Operates as an authorized user-notification and monitoring tool; does not perform unauthorized automated booking, ticket scalping, or bot bypasses.
  5. **🕰️ RewindWeb *(Cognitive Memory)* [In-Memory Search Prototype]**
     * Client-and-backend index enabling semantic concept queries (*"research paper on LLM memory"*) across previously browsed sessions.

---

## 🟩 SLIDE 4: TECHNICAL SPECIFICATIONS & SYSTEM PIPELINE

* **Slide Number:** `04 / 06`
* **Title:** **Engineering Architecture, Protocols, and Technical Scope**

* **Architecture Flow:**
  ```
  [User Input: Cursor Hover / Webcam Landmark / Push-to-Talk]
                               │
                               ▼
  [Chrome MV3 Extension] ──(Micro-DOM Slicer: ~2KB)──► [FastAPI Backend :8000]
                                                             │
          ┌──────────────────────────────────────────────────┼──────────────────────────────────────────────────┐
          ▼                                                  ▼                                                  ▼
  [SmartPoint / Swarm Router]                       [ElevenLabs Gateway]                               [GhostButler Daemon]
  - <150ms client-side DOM slicing                  - Sub-300ms vendor-quoted                         - Background monitoring loop
  - Focused ~400-600 token payload                    latency (Turbo v2.5 WebSocket)                   - WhatsApp webhook dispatch
  ```

* **Accurate Technical Benchmarks:**
  * **Client-Side Slicing Overhead:** **< 150 ms** for JavaScript to clean, prune SVGs/scripts, and clamp the hovered micro-DOM bounding box to under 2,500 characters. *(Note: Cloud LLM inference latency is additional and depends on the chosen provider).*
  * **Token Efficiency:** **~400–600 tokens** per micro-DOM query vs. thousands of tokens when transmitting full DOM trees.
  * **Computer Vision:** Continuous 30 FPS hand landmark tracking using Google MediaPipe WebAssembly.
  * **Automated Verification:** All 5 core API endpoints pass automated regression testing (`tests/test_api.py`).

* **Sponsor Alignment (wHACKiest 2026):**
  * **ElevenLabs:** Low-latency conversational speech streaming endpoint (`/ws/voice`) for audio feedback and voice navigation.
  * **AWS:** Microservices structured for containerized deployment on **AWS App Runner** or serverless execution via **AWS Lambda**.

---

## 🟩 SLIDE 5: COMPETITIVE LANDSCAPE & DIFFERENTIATION

* **Slide Number:** `05 / 06`
* **Title:** **Competitive Landscape: How AuraOS Differentiates**

* **Comparative Analysis:**

| Dimension | Claude in Chrome *(Anthropic)* | Coupon Extensions *(Honey, etc.)* | Web Monitors *(Visualping)* | Apple Vision Pro *(Safari)* | **AuraOS (Ours)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Interaction** | Full-browser agent across tabs | Script injection at cart checkout | Scheduled page screenshot diffs | Eye/hand tracking in headset | **Micro-DOM Lens + Spatial AirTouch** |
| **Hardware Required** | Standard PC | Standard PC | Cloud Server | **\$3,499 Headset** | **Zero Hardware (Standard Laptop Webcam)** |
| **Multi-Site Synthesis** | Yes (Agentic navigation) | ❌ Single checkout only | ❌ None | ❌ Single active window | **✅ Unified Comparison Card** |
| **Asynchronous Handoff**| ❌ Requires active session | ❌ Inactive | ⚠️ Email alerts (passive) | ❌ Inactive when headset off | **✅ Asynchronous WhatsApp Alert** |
| **Comprehension Mode** | Full-page visual analysis | Rule-based coupon matching | Pixel change detection | Standard web display | **In-place micro-DOM inspection** |

* **Defensible Positioning:**
  * While advanced general agents like *Claude in Chrome* navigate websites via full visual loops, *AuraOS* specializes in **targeted micro-DOM comprehension (inspecting specific components on hover)**, **hands-free webcam gesture control**, and **asynchronous mobile alert handoff**.

---

## 🟩 SLIDE 6: ETHICAL BOUNDARIES, FUTURE ROADMAP & PROPOSED SCOPE

* **Slide Number:** `06 / 06`
* **Title:** **Compliance Boundaries, Future Scope, and Proposed Roadmap**

* **Compliance & Technical Boundaries (Direct Defense for Judges):**
  * **Active Viewing vs. Background Monitoring:**
    * *SmartPoint & AirTouch* operate strictly within the user's active, authenticated browser tab, analyzing the specific element the user inspects.
    * *GhostButler* is designed strictly as a user-configured availability tracker that notifies the human user to take action, deliberately avoiding automated CAPTCHA solving, credential stuffing, or platform ToS violations.
  * **Local Privacy:** Micro-DOM extraction and history search are designed to run locally or via direct API connections without third-party data harvesting.

* **Proposed Future Roadmap (Subject to Post-Hackathon Development):**
  * **Phase 1 (Short-Term):** Migrate RewindWeb storage to a client-side WebAssembly vector engine (DuckDB/Wasm or IndexedDB) for fully offline, zero-latency local memory.
  * **Phase 2 (Medium-Term):** Expand AirTouch gesture sensitivity profiles to assist users with motor impairments in rehabilitation and assistive settings.
  * **Phase 3 (Long-Term):** Enterprise portal assistant: helping administrative users navigate legacy ERP and compliance forms that lack public APIs.

* **Proposed Business Model (Theoretical Projections):**
  * **Freemium B2C Model:** Free core desktop extension (SmartPoint + local RewindWeb); optional subscription tier (proposed at ₹299/mo) to offset cloud compute for continuous background monitoring.
