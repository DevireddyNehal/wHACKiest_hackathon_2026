/** AuraOS extension side panel: communicates with the local demo backend. */

const BACKEND_URL = "http://127.0.0.1:8000";
let currentMode = "DESK";
let currentMissionId = null;

document.addEventListener("DOMContentLoaded", () => {
  initHealthCheck();
  initModeSwitch();
  initTextCommand();
  initSwarmButton();
  initGhostButler();
  initRewindMemory();
});

async function request(path, options = {}) {
  const response = await fetch(`${BACKEND_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) }
  });
  let data = {};
  try { data = await response.json(); } catch { /* handled as an empty error response */ }
  if (!response.ok) {
    throw new Error(typeof data.detail === "string" ? data.detail : "The backend request failed.");
  }
  return data;
}

function initHealthCheck() {
  const dot = document.getElementById("backend-status-dot");
  const label = document.getElementById("backend-status-text");
  request("/health")
    .then(() => {
      dot.className = "status-dot live";
      label.textContent = "Local demo backend";
    })
    .catch(() => {
      dot.className = "status-dot dead";
      label.textContent = "Backend offline";
    });
}

function initModeSwitch() {
  const btnDesk = document.getElementById("btn-mode-desk");
  const btnAir = document.getElementById("btn-mode-air");
  const caption = document.getElementById("mode-caption");

  btnDesk.addEventListener("click", () => {
    currentMode = "DESK";
    btnDesk.classList.add("active");
    btnAir.classList.remove("active");
    caption.textContent = "Desk Mode: hover over an element and use the extension shortcut to analyze a small selected excerpt.";
    sendModeToContentScript("DESK");
  });

  btnAir.addEventListener("click", () => {
    currentMode = "AIR";
    btnAir.classList.add("active");
    btnDesk.classList.remove("active");
    caption.textContent = "Air Mode: pointer movement simulates a virtual laser. This prototype does not track hands or use the camera.";
    sendModeToContentScript("AIR");
  });
}

function sendModeToContentScript(mode) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]?.id) chrome.tabs.sendMessage(tabs[0].id, { type: "SET_MODE", mode });
  });
}

function initTextCommand() {
  const input = document.getElementById("voice-input");
  const sendBtn = document.getElementById("btn-voice-send");
  const sendCommand = () => {
    const text = input.value.trim();
    if (!text) return;
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, { type: "ANALYZE_MICRO_DOM", prompt: text });
      }
    });
    input.value = "";
  };
  sendBtn.addEventListener("click", sendCommand);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") sendCommand();
  });
}

function initSwarmButton() {
  const button = document.getElementById("btn-run-swarm");
  const box = document.getElementById("swarm-results-box");
  button.addEventListener("click", async () => {
    button.textContent = "Preparing sample…";
    button.disabled = true;
    try {
      const data = await request("/api/swarm/execute", {
        method: "POST",
        body: JSON.stringify({
          goal: "Compare sample flight options from Bengaluru to Delhi",
          target_sites: ["Direct carrier", "Travel marketplace", "Fare comparison"]
        })
      });
      box.replaceChildren();
      box.style.display = "block";
      const winner = document.createElement("div");
      winner.className = "winner-box";
      const title = document.createElement("strong");
      title.textContent = `Illustrative example: ${data.winner.platform}`;
      const detail = document.createElement("p");
      detail.textContent = `${data.winner.final_price} · ${data.winner.savings}`;
      winner.append(title, detail);
      box.append(winner);

      const rows = document.createElement("div");
      rows.className = "matrix-list";
      (data.comparison_matrix || []).forEach((item) => {
        const row = document.createElement("div");
        row.className = `matrix-row${item.is_best ? " best" : ""}`;
        const platform = document.createElement("span");
        platform.textContent = item.platform;
        const price = document.createElement("span");
        price.className = "price";
        price.textContent = item.total;
        row.append(platform, price);
        rows.append(row);
      });
      box.append(rows);
      const note = document.createElement("p");
      note.className = "card-desc";
      note.textContent = data.message;
      box.append(note);
    } catch (error) {
      box.replaceChildren(document.createTextNode(error.message));
      box.style.display = "block";
    } finally {
      button.textContent = "Show sample comparison";
      button.disabled = false;
    }
  });
}

async function initGhostButler() {
  const pill = document.getElementById("active-mission-pill");
  const pillText = pill.querySelector("span:last-child");
  const button = document.getElementById("btn-trigger-whatsapp");
  const preview = document.getElementById("whatsapp-preview-box");
  try {
    const missions = await request("/api/butler/missions");
    const mission = missions[0];
    if (!mission) {
      pillText.textContent = "No demo reminder available";
      button.disabled = true;
      return;
    }
    currentMissionId = mission.id;
    pillText.textContent = `${mission.title} · demo only`;
  } catch (error) {
    pillText.textContent = error.message;
    button.disabled = true;
  }

  button.addEventListener("click", async () => {
    if (!currentMissionId) return;
    const confirmed = window.confirm("Preview a simulated in-app alert? No site will be checked and no booking or payment will happen.");
    if (!confirmed) return;
    button.disabled = true;
    try {
      const data = await request("/api/butler/missions/trigger-demo", {
        method: "POST",
        body: JSON.stringify({ mission_id: currentMissionId, confirmed: true })
      });
      preview.replaceChildren();
      preview.style.display = "block";
      const bubble = document.createElement("div");
      bubble.className = "whatsapp-bubble";
      const title = document.createElement("div");
      title.className = "wa-header";
      title.textContent = "In-app demo alert · not sent";
      const message = document.createElement("p");
      message.className = "wa-body";
      message.textContent = data.notification.message;
      bubble.append(title, message);
      preview.append(bubble);
    } catch (error) {
      preview.textContent = error.message;
      preview.style.display = "block";
    } finally {
      button.disabled = false;
    }
  });
}

function initRewindMemory() {
  const input = document.getElementById("memory-search-input");
  const list = document.getElementById("memory-list-box");
  let timer;
  const fetchMemory = async (query = "") => {
    try {
      const data = await request("/api/memory/search", {
        method: "POST",
        body: JSON.stringify({ query })
      });
      list.replaceChildren();
      if (!data.results.length) {
        list.append(document.createTextNode("No matching notes. Try another phrase."));
        return;
      }
      data.results.forEach((item) => {
        const card = document.createElement("div");
        card.className = "memory-card";
        const tag = document.createElement("span");
        tag.className = "mem-tag";
        tag.textContent = item.category;
        const title = document.createElement("strong");
        title.className = "mem-title";
        title.textContent = item.title;
        const snippet = document.createElement("p");
        snippet.className = "mem-snippet";
        snippet.textContent = item.snippet;
        const timestamp = document.createElement("span");
        timestamp.className = "mem-time";
        timestamp.textContent = item.timestamp;
        card.append(tag, title, snippet, timestamp);
        list.append(card);
      });
    } catch (error) {
      list.replaceChildren(document.createTextNode(error.message));
    }
  };
  fetchMemory();
  input.addEventListener("input", (event) => {
    clearTimeout(timer);
    timer = setTimeout(() => fetchMemory(event.target.value.trim()), 180);
  });
}
