/**
 * AuraOS SidePanel Command Center Logic
 * Unifies all 5 pillars with real-time state and backend synchronization.
 */

const BACKEND_URL = "http://127.0.0.1:8000";
let currentMode = "DESK";

document.addEventListener("DOMContentLoaded", () => {
  initHealthCheck();
  initModeSwitch();
  initVoiceInput();
  initSwarmButton();
  initGhostButler();
  initRewindMemory();
});

// 1. Backend Health Check
function initHealthCheck() {
  const dot = document.getElementById("backend-status-dot");
  const label = document.getElementById("backend-status-text");

  fetch(`${BACKEND_URL}/health`)
    .then((res) => res.json())
    .then((data) => {
      dot.className = "status-dot live";
      label.textContent = "Backend Live (Port 8000)";
    })
    .catch(() => {
      dot.className = "status-dot dead";
      label.textContent = "Backend Offline";
    });
}

// 2. Mode Switcher (Desk vs Air)
function initModeSwitch() {
  const btnDesk = document.getElementById("btn-mode-desk");
  const btnAir = document.getElementById("btn-mode-air");
  const caption = document.getElementById("mode-caption");

  btnDesk.addEventListener("click", () => {
    currentMode = "DESK";
    btnDesk.classList.add("active");
    btnAir.classList.remove("active");
    caption.innerHTML = "<strong>Desk Mode:</strong> Hover cursor over any element + press <code>Alt+S</code> to unmask fees & traps.";
    sendModeToContentScript("DESK");
  });

  btnAir.addEventListener("click", () => {
    currentMode = "AIR";
    btnAir.classList.add("active");
    btnDesk.classList.remove("active");
    caption.innerHTML = "<strong>Air Mode (Active):</strong> Raise hand to point virtual laser. Pinch fingers to click. Palm swipe to scroll.";
    sendModeToContentScript("AIR");
  });
}

function sendModeToContentScript(mode) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]?.id) {
      chrome.tabs.sendMessage(tabs[0].id, { type: "SET_MODE", mode });
    }
  });
}

// 3. Voice Command Bar
function initVoiceInput() {
  const input = document.getElementById("voice-input");
  const sendBtn = document.getElementById("btn-voice-send");
  const micBtn = document.getElementById("btn-mic-toggle");

  const sendCommand = () => {
    const text = input.value.trim();
    if (!text) return;

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, {
          type: "ANALYZE_MICRO_DOM",
          prompt: text
        });
      }
    });

    input.value = "";
  };

  sendBtn.addEventListener("click", sendCommand);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendCommand();
  });

  micBtn.addEventListener("click", () => {
    micBtn.classList.toggle("listening");
    if (micBtn.classList.contains("listening")) {
      input.placeholder = "Listening via ElevenLabs Conversational Voice...";
    } else {
      input.placeholder = "Speak or type intent...";
    }
  });
}

// 4. Pillar 3: Multi-Tab Swarm
function initSwarmButton() {
  const btn = document.getElementById("btn-run-swarm");
  const box = document.getElementById("swarm-results-box");

  btn.addEventListener("click", () => {
    btn.textContent = "Scanning 3 parallel sites...";
    btn.disabled = true;

    fetch(`${BACKEND_URL}/api/swarm/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        goal: "Find cheapest direct flight Bangalore to Delhi with 15kg baggage",
        target_sites: ["MakeMyTrip", "IndiGo Direct", "EaseMyTrip"]
      })
    })
      .then((res) => res.json())
      .then((data) => {
        btn.textContent = "Execute Parallel Swarm";
        btn.disabled = false;
        box.style.display = "block";

        let matrixRows = data.comparison_matrix.map(m => `
          <div class="matrix-row ${m.is_best ? 'best' : ''}">
            <span>${m.platform}</span>
            <span class="price">${m.total} ${m.is_best ? '🏆' : ''}</span>
          </div>
        `).join("");

        box.innerHTML = `
          <div class="winner-box">
            <strong>${data.winner.platform} Wins</strong>
            <p>${data.winner.savings} (${data.winner.final_price} total with baggage)</p>
          </div>
          <div class="matrix-list">${matrixRows}</div>
          <div class="consent-pill">🛡️ Consent Shield Active: 1-Click Pay Ready</div>
        `;
      })
      .catch(() => {
        btn.textContent = "Execute Parallel Swarm";
        btn.disabled = false;
      });
  });
}

// 5. Pillar 4: GhostButler Background Tasks
function initGhostButler() {
  const triggerBtn = document.getElementById("btn-trigger-whatsapp");
  const previewBox = document.getElementById("whatsapp-preview-box");

  triggerBtn.addEventListener("click", () => {
    triggerBtn.textContent = "Triggering Background Event...";

    fetch(`${BACKEND_URL}/api/butler/missions/trigger-demo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mission_id: "mission_tatkal_demo" })
    })
      .then((res) => res.json())
      .then((data) => {
        triggerBtn.textContent = "Simulate Slot Trigger & WhatsApp";
        previewBox.style.display = "block";
        const notif = data.notification;
        previewBox.innerHTML = `
          <div class="whatsapp-bubble">
            <div class="wa-header">📲 WhatsApp Message Dispatched (${notif.recipient})</div>
            <pre class="wa-body">${notif.message}</pre>
          </div>
        `;
      });
  });
}

// 6. Pillar 5: RewindWeb Memory
function initRewindMemory() {
  const input = document.getElementById("memory-search-input");
  const list = document.getElementById("memory-list-box");

  const fetchMemory = (q = "") => {
    fetch(`${BACKEND_URL}/api/memory/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    })
      .then((res) => res.json())
      .then((data) => {
        list.innerHTML = data.results.map(r => `
          <div class="memory-card">
            <span class="mem-tag">${r.category}</span>
            <strong class="mem-title">${r.title}</strong>
            <p class="mem-snippet">${r.snippet}</p>
            <span class="mem-time">${r.timestamp}</span>
          </div>
        `).join("");
      });
  };

  fetchMemory();

  input.addEventListener("input", (e) => {
    fetchMemory(e.target.value.trim());
  });
}
