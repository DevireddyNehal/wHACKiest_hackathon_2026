# 📊 wHACKiest 2026 — Slide Deck Content (`TeamName_Track2.pptx`)
> **Track:** Track 02 — Beyond the Browser  
> **Repository:** https://github.com/DevireddyNehal/wHACKiest_hackathon_2026  
> **Scope:** Grounded claims, transparent prototype status, verified citations.

---

## SLIDE 1: COVER SLIDE
* **Slide Number:** 01 / 06
* **Title:** AuraOS
* **Subtitle:** The Autonomous Web Operating System: Reimagining how users perceive, navigate, and delegate web workflows.
* **Track:** Track 02 — Beyond the Browser (Focus: Browser Agents · Web Automation · Accessibility · Search)
* **Team:** [Your Team Name] | Department of CSE, Ramaiah Institute of Technology, Bengaluru
* **Repository:** https://github.com/DevireddyNehal/wHACKiest_hackathon_2026

---

## SLIDE 2: THE PROBLEM (EVIDENCE & CONTEXT)
* **Slide Number:** 02 / 06
* **Title:** The Friction of the Modern Web: Cognitive Load, Deception, and Inefficiency
* **Documented Context:**
  * Dark Patterns Prevalence: An empirical study of ~11,000 shopping websites found that 11.1% (1,254 sites) featured dark patterns across 1,818 instances, with more popular shopping sites found to be more likely to feature them (Mathur et al., ACM CSCW 2019).
  * Regulatory Action: In November 2023, the Indian Ministry of Consumer Affairs (DoCA) formally issued Guidelines for the Prevention and Regulation of Dark Patterns under the Consumer Protection Act, prohibiting deceptive practices including drip pricing, hidden costs, and false urgency.
  * High-Demand Workflows: Routine online contention points (such as railway Tatkal booking drops, limited flash sales, and registration openings) face high server demand and rapid sell-outs, leaving users vulnerable to manual delays or input errors.
  * Web Agent Inefficiencies: Visual browser agents that transmit entire full-page screenshots or full DOM trees incur substantial token footprint and latency compared to targeted element extraction.
* **Core Pain Points:**
  1. Manual Data Routing: Comparing products or travel requires juggling multiple tabs and manually extracting details across inconsistent layouts.
  2. Drip Pricing: Displayed prices often exclude mandatory fees or add-ons until late in the checkout flow.
  3. The Babysitting Burden: Users must actively watch and refresh dynamic portals instead of delegating the wait to an automated assistant.
  4. Accessibility Barriers: Complex, ad-heavy web applications present high physical friction for users with motor tremors or repetitive strain injuries (RSI).

---

## SLIDE 3: THE PROPOSED SOLUTION — AURAOS (THE 5 PILLARS)
* **Slide Number:** 03 / 06
* **Title:** AuraOS: A Unified Architecture Across Time, Space, and Autonomy
* **Core Idea:** AuraOS decouples web intent and execution from visual clutter, providing tools for immediate inspection, hands-free interaction, and asynchronous delegation.
* **The 5 Pillars & Implementation Status:**
  1. SmartPoint (Desk Mode — Micro-Comprehension) [Functional Prototype]
     - Hover over any webpage element and press Alt+S.
     - Extracts the hovered micro-DOM node, unmasking hidden fees, terms, or complex text in a frosted-glass popover card.
     - Implementation: Live in-browser DOM extraction via Chrome extension; backend supports live LLM API calls with deterministic mock fallbacks for offline demo reliability.
  2. AirTouch (Air Mode — Hands-Free Interaction) [Experimental Prototype]
     - Integrates Google MediaPipe Hands via standard laptop webcam.
     - Projects a virtual laser pointer from the index finger with pinch-to-click and palm-scroll handlers for touch-free accessibility.
  3. SynapseWeb (Multi-Tab Execution) [Prototype Orchestrator]
     - Backend orchestrator that models parallel execution across competitor sites (e.g., direct carrier vs. aggregator).
     - Synthesizes cross-site data into a single comparison card with an explicit Consent Shield halting before payments.
  4. GhostButler (Asynchronous Delegation) [Architecture & Notification Prototype]
     - Background monitoring daemon that tracks portal availability and dispatches simulated (logged) WhatsApp alerts, live if Twilio credentials are configured.
     - Compliance Boundary: Designed strictly as an availability monitoring and alert assistant; does not perform automated booking, captcha circumvention, or bot bypasses.
  5. RewindWeb (Cognitive Memory) [In-Memory Search Prototype]
     - In-memory search index allowing natural language concept queries across previously browsed sessions.

---

## SLIDE 4: TECHNICAL SPECIFICATIONS & SYSTEM PIPELINE
* **Slide Number:** 04 / 06
* **Title:** Engineering Architecture, Protocols, and Technical Scope
* **Architecture Flow:**
  [User Input: Cursor Hover / Webcam Landmark / Push-to-Talk]
            │
            ▼
  [Chrome MV3 Extension] ──(Micro-DOM Slicer)──► [FastAPI Backend :8000]
                                                        │
      ┌─────────────────────────────────────────────────┼─────────────────────────────────────────────────┐
      ▼                                                 ▼                                                 ▼
  [SmartPoint / Swarm Router]                  [ElevenLabs Gateway]                              [GhostButler Daemon]
  - Targeted micro-DOM extraction              - Conversational speech                           - Background monitoring loop
  - Bounding-box sanitization                    streaming via WebSocket                         - Simulated WhatsApp alert
* **Engineering Properties:**
  - Local DOM Slicing: Client-side JavaScript prunes SVGs and scripts, extracting only the isolated target element to reduce payload size before transmission.
  - Computer Vision: Hand landmark tracking using Google MediaPipe WebAssembly.
  - Automated Smoke Testing: Backend endpoints for pillars 1, 3, 4, and 5 pass automated regression smoke tests (tests/test_api.py); AirTouch is tested manually via client-side DOM events.
* **Sponsor Alignment (wHACKiest 2026):**
  - ElevenLabs: Low-latency conversational speech streaming endpoint (/ws/voice) for audio feedback and voice navigation.
  - AWS: Microservices structured for containerized deployment on AWS App Runner or serverless execution via AWS Lambda.

---

## SLIDE 5: COMPETITIVE LANDSCAPE & DIFFERENTIATION
* **Slide Number:** 05 / 06
* **Title:** Competitive Landscape: How AuraOS Differentiates
* **Comparative Overview:**
  - Primary Interaction:
    • Claude in Chrome: Full-browser agent across tabs
    • Coupon Extensions (Honey, etc.): Script injection at cart checkout
    • Web Monitors (Visualping): Scheduled page screenshot diffs
    • Apple Vision Pro (Safari): Eye/hand tracking in headset
    • AuraOS (Ours): Micro-DOM Lens + Spatial AirTouch
  - Hardware Required:
    • Claude in Chrome: Standard PC
    • Coupon Extensions: Standard PC
    • Web Monitors: Cloud Server
    • Apple Vision Pro: $3,499 Headset
    • AuraOS: Zero Hardware (Standard Laptop Webcam)
  - Multi-Site Synthesis:
    • Claude in Chrome: Supported
    • Coupon Extensions: Single checkout only
    • Web Monitors: None
    • Apple Vision Pro: Single active window
    • AuraOS: Unified Comparison Card
  - Asynchronous Handoff:
    • Claude in Chrome: Active session only
    • Coupon Extensions: Inactive
    • Web Monitors: Email alerts (passive)
    • Apple Vision Pro: Inactive when headset off
    • AuraOS: Asynchronous WhatsApp Alert (Simulated)
* **Positioning:**
  While full-browser agents like Claude in Chrome automate general workflows across tabs, AuraOS focuses on targeted in-place micro-DOM inspection on hover, hardware-free webcam gesture control without headsets, and asynchronous mobile alert delegation.

---

## SLIDE 6: COMPLIANCE, FUTURE ROADMAP & PROPOSED SCOPE
* **Slide Number:** 06 / 06
* **Title:** Compliance Boundaries, Future Scope, and Proposed Roadmap
* **Compliance Boundaries (Judge Defense):**
  - Active Viewing vs. Background Monitoring:
    • SmartPoint & AirTouch operate strictly within the user's active, authenticated browser tab, analyzing the specific element the user inspects.
    • GhostButler is designed strictly as an availability monitoring assistant that alerts the user to take action, deliberately avoiding automated CAPTCHA solving, credential stuffing, or platform ToS violations.
  - Data Privacy: SmartPoint transmits only the focused micro-DOM snippet directly to the configured endpoint (or local mock), avoiding full-page history uploads.
* **Proposed Future Roadmap:**
  - Phase 1 (Short-Term): Migrate RewindWeb storage to a client-side WebAssembly vector engine (DuckDB/Wasm or IndexedDB) for fully offline local memory.
  - Phase 2 (Medium-Term): Explore adapting AirTouch gesture sensitivity profiles as an accessibility exploration for users with motor impairments.
  - Phase 3 (Long-Term): Enterprise portal assistant: exploring assistive workflows for administrative users navigating legacy ERP and compliance forms that lack public APIs.
* **Proposed Business Model (Theoretical Projections):**
  - Freemium Model: Free core desktop extension (SmartPoint + local RewindWeb); optional subscription tier (proposed at ₹299/mo) to offset cloud compute for continuous background monitoring.
