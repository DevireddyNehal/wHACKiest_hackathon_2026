/**
 * AuraOS Pillar 1: SmartPoint (Desk Mode)
 * Ultra-fast micro-DOM extraction and contextual popover HUD (<200ms).
 */

class SmartPointEngine {
  constructor() {
    this.currentHoveredElement = null;
    this.hudElement = null;
    this.isAnalyzing = false;
    this.initListeners();
    console.log("✓ AuraOS SmartPoint (Desk Mode) initialized");
  }

  initListeners() {
    // 1. Track hover position
    document.addEventListener("mouseover", (e) => {
      if (this.hudElement && this.hudElement.contains(e.target)) return;
      this.currentHoveredElement = e.target;
    }, { passive: true });

    // 2. Keyboard shortcut: Alt + S or Double-Shift to trigger SmartPoint on hovered item
    document.addEventListener("keydown", (e) => {
      if (e.altKey && (e.key === "s" || e.key === "S")) {
        e.preventDefault();
        this.triggerAnalysis();
      }
      if (e.key === "Escape") {
        this.removeHUD();
      }
    });

    // 3. Listen for message from Extension Hotkey
    chrome.runtime.onMessage.addListener((msg) => {
      if (msg.type === "TRIGGER_SMARTPOINT") {
        this.triggerAnalysis();
      }
    });
  }

  triggerAnalysis() {
    if (!this.currentHoveredElement || this.isAnalyzing) return;
    this.isAnalyzing = true;

    // Visual pulse on the targeted element
    this.currentHoveredElement.classList.add("aura-pulse-target");

    // Slices only the micro-DOM under cursor (max 2000 chars)
    const domSnippet = this.extractMicroDOM(this.currentHoveredElement);
    const rect = this.currentHoveredElement.getBoundingClientRect();

    // Show loading HUD
    this.showHUD(rect.left + window.scrollX, rect.bottom + window.scrollY + 8, null, true);

    // Call Background Service Worker
    chrome.runtime.sendMessage(
      {
        type: "ANALYZE_MICRO_DOM",
        dom_snippet: domSnippet,
        prompt: "Analyze this element: audit hidden fees, explain cryptic terms, and flag dark patterns"
      },
      (res) => {
        this.isAnalyzing = false;
        if (this.currentHoveredElement) {
          this.currentHoveredElement.classList.remove("aura-pulse-target");
        }

        if (res && res.success && res.data) {
          this.showHUD(rect.left + window.scrollX, rect.bottom + window.scrollY + 8, res.data, false);
        } else {
          this.showErrorHUD(rect.left + window.scrollX, rect.bottom + window.scrollY + 8, res?.error || "Analysis failed");
        }
      }
    );
  }

  extractMicroDOM(el) {
    const clone = el.cloneNode(true);
    // Remove heavy SVGs and scripts
    clone.querySelectorAll("svg, script, style, noscript, iframe").forEach(n => n.remove());
    let html = clone.outerHTML || el.innerText || "";
    if (html.length > 2500) {
      html = html.substring(0, 2500) + "... [truncated]";
    }
    return html;
  }

  showHUD(x, y, data, isLoading) {
    this.removeHUD();

    this.hudElement = document.createElement("div");
    this.hudElement.className = "aura-smartpoint-hud";
    this.hudElement.style.left = `${Math.min(x, window.innerWidth - 380)}px`;
    this.hudElement.style.top = `${y}px`;

    if (isLoading) {
      this.hudElement.innerHTML = `
        <div class="aura-hud-header">
          <span class="aura-badge loading">✨ SmartPoint AI</span>
          <span class="aura-hud-close">&times;</span>
        </div>
        <div class="aura-hud-loading">
          <div class="aura-spinner"></div>
          <span>Analyzing micro-DOM context...</span>
        </div>
      `;
    } else {
      let breakdownHtml = "";
      if (data.breakdown && Array.isArray(data.breakdown)) {
        breakdownHtml = data.breakdown.map(b => `
          <div class="aura-breakdown-row ${b.warning ? 'warn' : ''} ${b.highlight ? 'highlight' : ''}">
            <span class="aura-item-name">${b.item}</span>
            <span class="aura-item-val">${b.amount}</span>
          </div>
        `).join("");
      }

      this.hudElement.innerHTML = `
        <div class="aura-hud-header">
          <span class="aura-badge ${data.category === 'DARK_PATTERN_WARNING' ? 'bad' : 'ok'}">${data.badge}</span>
          <span class="aura-hud-close" id="aura-close-btn">&times;</span>
        </div>
        <h4 class="aura-hud-title">${data.title}</h4>
        <p class="aura-hud-summary">${data.summary}</p>
        <div class="aura-hud-breakdown">
          ${breakdownHtml}
        </div>
        <div class="aura-hud-footer">
          <span class="aura-hud-rec">💡 ${data.action_recommendation}</span>
          <span class="aura-hud-latency">${data.latency_ms}ms</span>
        </div>
      `;
    }

    document.body.appendChild(this.hudElement);

    const closeBtn = this.hudElement.querySelector(".aura-hud-close");
    if (closeBtn) {
      closeBtn.onclick = () => this.removeHUD();
    }
  }

  showErrorHUD(x, y, errorMsg) {
    this.removeHUD();
    this.hudElement = document.createElement("div");
    this.hudElement.className = "aura-smartpoint-hud";
    this.hudElement.style.left = `${x}px`;
    this.hudElement.style.top = `${y}px`;
    this.hudElement.innerHTML = `
      <div class="aura-hud-header">
        <span class="aura-badge bad">Connection Notice</span>
        <span class="aura-hud-close" id="aura-close-btn">&times;</span>
      </div>
      <p class="aura-hud-summary">Backend offline. Please start local backend: <code>python backend/main.py</code></p>
    `;
    document.body.appendChild(this.hudElement);
    this.hudElement.querySelector(".aura-hud-close").onclick = () => this.removeHUD();
  }

  removeHUD() {
    if (this.hudElement && this.hudElement.parentNode) {
      this.hudElement.parentNode.removeChild(this.hudElement);
      this.hudElement = null;
    }
  }
}

window.auraSmartPoint = new SmartPointEngine();
