# 🏗️ AuraOS — System Architecture & Technical Specifications

> **wHACKiest 2026 Hackathon | Track 02: Beyond the Browser**  
> Comprehensive technical guide detailing the micro-services, messaging protocols, and algorithms.

---

## 1. High-Level System Architecture

AuraOS follows a **Decoupled Edge-Agent Architecture**:
* **Client-Side (Edge):** Chrome Manifest V3 Extension (Content Scripts, Virtual DOM Slicing, MediaPipe Gesture Raycasting, Frosted-Glass Popover HUD).
* **Control Plane:** Manifest V3 Background Service Worker routing events between the active tab and the FastAPI orchestrator.
* **Orchestration Engine:** Python FastAPI server handling micro-DOM LLM inferences, parallel swarm workers, and ElevenLabs full-duplex WebSocket connections.
* **Asynchronous Execution:** Headless worker loops for 24/7 background slot monitoring, queue sniping, and WhatsApp webhooks.

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
1. Receives user high-level goal: *"Find cheapest direct flight Bangalore to Delhi under ₹6,000"*.
2. Swarm coordinator spawns parallel headless sessions across target competitor domains:
   * Worker A: Aggregator (e.g., MakeMyTrip).
   * Worker B: Direct Carrier (e.g., IndiGo).
   * Worker C: Discount Portal (e.g., EaseMyTrip).
3. Evaluates down to the **payment gateway stage** to expose hidden convenience fees, fuel surcharges, and baggage add-ons.
4. Synthesizes a structured `ComparisonMatrix` payload with a designated `winner` and true total prices.
5. Emits `prefilled_cart_ready` with a **Consent Shield** waiting for the user's 1-click payment confirmation.

---

### Subsystem 4: GhostButler (Asynchronous Cloud Daemon)
1. User activates mission via Chrome Extension or WhatsApp: *"Snipe Tatkal 3AC seats for Bangalore to Chennai on Nov 28"*.
2. Mission stored in background execution registry (`/api/butler/missions`).
3. Autonomous loop wakes up at 09:59:58 AM IST.
4. Navigates queue bypass holding pattern, parses captcha, auto-fills passenger details in 1.2 seconds.
5. Holds seats for the 4-minute checkout window.
6. Dispatches instant **WhatsApp notification via Twilio/Meta API** with a 1-tap UPI payment link.

---

### Subsystem 5: RewindWeb (Client-Side Semantic Memory)
1. Intercepts page navigations and user interactions.
2. Extracts core text, meta tags, and visual preview.
3. Indexes content into a lightweight vector store (IndexedDB on client or server-side memory index).
4. Enables natural language semantic search across browsing history (`/api/memory/search`) without requiring exact URL matches.

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
