# 🏗️ AuraOS — System Architecture & Technical Specifications

> **wHACKiest 2026 Hackathon | Track 02: Beyond the Browser**  
> Comprehensive technical guide detailing the micro-services, messaging protocols, and algorithms.

---

> **Status:** This is a target-state design document, not a description of the current executable prototype. The dashboard uses simulated comparisons, pointer-only AirTouch, text-only demo memory, and a manually confirmed in-app GhostButler preview. It does not monitor sites, bypass queues or access controls, book, message externally, or initiate payment.

## 1. High-Level System Architecture

AuraOS follows a **Decoupled Edge-Agent Architecture**:
* **Client-Side (Edge):** Chrome Manifest V3 Extension (Content Scripts, Virtual DOM Slicing, MediaPipe Gesture Raycasting, Frosted-Glass Popover HUD).
* **Control Plane:** Manifest V3 Background Service Worker routing events between the active tab and the FastAPI orchestrator.
* **Orchestration Engine:** Python FastAPI server handling micro-DOM LLM inferences, parallel swarm workers, and ElevenLabs full-duplex WebSocket connections.
* **Asynchronous Execution (proposed):** Future reminder and alert services, subject to official APIs and explicit user confirmation.

```
+---------------------------------------------------------------------------------------+
|                                CHROME BROWSER EXTENSION                               |
|                                                                                       |
|   +--------------------------+       +---------------------+   +------------------+   |
|   |   SmartPoint Engine      |       |   AirTouch Engine   |   |   SidePanel UI   |   |
|   |  - Micro-DOM Bounding Box|       |  - MediaPipe Hands  |   |  - Mode Switch   |   |
|   |  - Bounding Rect Slicing |       |  - Laser Raycasting |   |  - Audio Wave    |   |
|   |  - Alt+S / Double-Shift  |       |  - Pinch / Swipe    |   |  - Swarm Monitor |   |
|   +------------+-------------+       +----------+----------+   +--------+---------+   |
|                |                                |                       |             |
|                +--------------------------------+-----------------------+             |
|                                                 | Chrome Runtime Relay                |
|                                                 v                                     |
|                                  +------------------------------+                     |
|                                  | Background Service Worker    |                     |
|                                  +--------------+---------------+                     |
+-------------------------------------------------|-------------------------------------+
                                                  | REST / WebSocket (:8000)
                                                  v
+---------------------------------------------------------------------------------------+
|                                FASTAPI BACKEND SERVER                                 |
|                                                                                       |
|   +-----------------------+   +----------------------+   +------------------------+   |
|   |  /api/smartpoint      |   |  /api/swarm          |   |  /api/butler           |   |
|   |  - Micro-DOM Parser   |   |  - Multi-Tab Runner  |   |  - Slot & Queue Sniper |   |
|   |  - Fee Unmasking      |   |  - Cross-Site Matrix |   |  - WhatsApp Webhook    |   |
|   +-----------+-----------+   +----------+-----------+   +-----------+------------+   |
|               |                          |                           |                |
|               +--------------------------+---------------------------+                |
|                                          |                                            |
|                 +------------------------+-----------------------+                    |
|                 |                                                |                    |
|                 v                                                v                    |
|   +----------------------------+                   +------------------------------+   |
|   |   ElevenLabs Audio Gateway |                   |   Cloud / External Services  |   |
|   |   - Sub-300ms Conversational|                  |   - AWS Lambda / Bedrock     |   |
|   |   - Low-latency Audio Stream|                  |   - Twilio WhatsApp API      |   |
|   +----------------------------+                   +------------------------------+   |
+---------------------------------------------------------------------------------------+
```

---

## 2. Deep Dive: The 5 Core Subsystems

### Subsystem 1: SmartPoint (Micro-DOM Extraction Algorithm)
Traditional browser agents dump the entire 400KB HTML DOM or upload full 4K screenshots to an LLM. This causes 8–15 second delays, costs thousands of tokens, and causes hallucination on cluttered pages.

**SmartPoint's Slicing Algorithm:**
1. Tracks cursor coordinates `(x, y)` via passive `mouseover` listeners.
2. Identifies target element: `el = document.elementFromPoint(x, y)`.
3. Resolves semantic boundary: Finds nearest interactive or structural container (`button`, `a`, `div.card`, `p`, `tr`).
4. Strips all `<svg>`, `<script>`, `<style>`, `<iframe>`, and empty comment nodes.
5. Clamps outerHTML payload to **under 2,500 characters** (< 600 tokens).
6. Dispatches to `/api/smartpoint/analyze`.
7. **Result:** Inferences complete in **< 150ms** with 95% token savings.

---

### Subsystem 2: AirTouch (Spatial Raycasting & Gesture Mapping)
1. **Camera Frame Pipeline:** Standard webcam video stream captured at 30 FPS.
2. **MediaPipe Hand Landmark Extraction:** Tracks 21 3D hand joints (`wrist`, `index_tip`, `thumb_tip`, etc.).
3. **Laser Projection:** Raycasts normalized coordinates of Landmark 8 (Index Finger Tip) onto the browser viewport.
4. **Anti-Jitter Exponential Moving Average (EMA):**
   $$\text{smoothedX} = \text{smoothedX} \times 0.7 + \text{rawX} \times 0.3$$
   $$\text{smoothedY} = \text{smoothedY} \times 0.7 + \text{rawY} \times 0.3$$
5. **Gesture Trigger Engine:**
   * **Pinch Click:** Calculated via Euclidean distance between Index Tip (8) and Thumb Tip (4):
     $$\text{dist} = \sqrt{(x_8 - x_4)^2 + (y_8 - y_4)^2}$$
     If $\text{dist} < \text{threshold}$, fires synthetic `target.click()`.
   * **Palm Swipe:** Velocity vector of Palm Center (0) triggers `window.scrollBy({ behavior: 'smooth' })`.

---

### Subsystem 3: SynapseWeb Multi-Tab Swarm
The current endpoint returns a labeled illustrative comparison matrix. It does not open tabs, inspect checkout pages, verify prices, prefill a cart, or perform transactions. A future implementation should use permitted data sources and present results as unverified until the user checks the provider.

---

### Subsystem 4: GhostButler (Asynchronous Cloud Daemon)
The current endpoint stores reminder templates in process memory and returns an in-app alert preview only after explicit confirmation. There is no scheduler or external notification integration in the dashboard. Any future availability feature must use official interfaces, respect queues and access controls, and stop before booking or payment.

---

### Subsystem 5: RewindWeb (Client-Side Semantic Memory)
The current implementation stores only titles, optional URLs, and short excerpts explicitly submitted by the user. It uses keyword matching in process memory; no browser history, screenshots, snapshots, or embeddings are collected.

---

## 3. Technology Stack & Dependencies

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Extension Framework** | Chrome Manifest V3 (Vanilla JS, CSS3, HTML5) | Native performance, zero build-step overhead, instant Chrome loading. |
| **Backend API** | Python 3.10+ / FastAPI / Uvicorn | Ultra-fast async I/O, native WebSocket streaming, automatic OpenAPI documentation. |
| **Computer Vision** | Google MediaPipe Hands (WebAssembly / TF.js) | Sub-30ms landmark tracking running completely client-side in the browser. |
| **Conversational Voice**| **ElevenLabs Conversational Voice API** | Sub-300ms bidirectional speech streaming and human-grade vocal synthesis. |
| **Cloud & Serverless** | **AWS Lambda / ECS / App Runner / Bedrock** | Scalable serverless execution for headless background worker loops. |
| **Notifications** | Twilio / Meta WhatsApp Business API | Frictionless 1-tap mobile notifications for everyday non-technical users. |
