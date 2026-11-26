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
      } else if (msg.type === "ANALYZE_MICRO_DOM") {
        this.triggerAnalysis(msg.prompt);
      }
    });
  }

  triggerAnalysis(userPrompt = "Explain this selected text") {
    if (!this.currentHoveredElement || this.isAnalyzing) return;
    this.isAnalyzing = true;

    // Visual pulse on the targeted element
    this.currentHoveredElement.classList.add("aura-pulse-target");

    // Slices only the micro-DOM under cursor (max 2000 chars)
    const domSnippet = this.extractMicroDOM(this.currentHoveredElement);
    this.lastSnippet = domSnippet;
    this.lastPageUrl = location.href;
    const rect = this.currentHoveredElement.getBoundingClientRect();

    // Show loading HUD
    this.showHUD(rect.left + window.scrollX, rect.bottom + window.scrollY + 8, null, true);

    // Call Background Service Worker
    chrome.runtime.sendMessage(
      {
        type: "ANALYZE_MICRO_DOM",
        dom_snippet: domSnippet,
        prompt: userPrompt
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
    clone.querySelectorAll("svg, script, style, noscript, iframe").forEach(n => n.remove());
    const visible = (clone.innerText || clone.textContent || "").replace(/\s+/g, " ").trim();
    if (visible) return visible.slice(0, 2500);
    return (clone.outerHTML || "").slice(0, 2500);
  }

  showHUD(x, y, data, isLoading) {
    this.removeHUD();

    this.hudElement = document.createElement("div");
    this.hudElement.className = "aura-smartpoint-hud";
    this.hudElement.style.width = `${Math.min(360, window.innerWidth - 24)}px`;
    this.hudElement.style.left = `${Math.max(8, Math.min(x, window.innerWidth - 368))}px`;
    this.hudElement.style.top = `${y}px`;

    const header = document.createElement("div");
    header.className = "aura-hud-header";
    const badge = document.createElement("span");
    const close = document.createElement("button");
    close.type = "button";
    close.className = "aura-hud-close";
    close.setAttribute("aria-label", "Close SmartPoint");
    close.textContent = "×";
    close.addEventListener("click", () => this.removeHUD());

    if (isLoading) {
      badge.className = "aura-badge loading";
      badge.textContent = "SmartPoint demo";
      header.append(badge, close);
      const loading = document.createElement("div");
      loading.className = "aura-hud-loading";
      const spinner = document.createElement("div");
      spinner.className = "aura-spinner";
      const label = document.createElement("span");
      label.textContent = "Analyzing selected text…";
      loading.append(spinner, label);
      this.hudElement.append(header, loading);
    } else {
      badge.className = `aura-badge ${data.category === "DARK_PATTERN_WARNING" ? "bad" : "ok"}`;
      badge.textContent = data.badge || "Demo analysis";
      header.append(badge, close);
      const title = document.createElement("h4");
      title.className = "aura-hud-title";
      title.textContent = data.title || "Selected text";
      const summary = document.createElement("p");
      summary.className = "aura-hud-summary";
      summary.textContent = data.summary || "";
      const breakdown = document.createElement("div");
      breakdown.className = "aura-hud-breakdown";
      (Array.isArray(data.breakdown) ? data.breakdown : []).forEach((item) => {
        const row = document.createElement("div");
        row.className = `aura-breakdown-row${item.warning ? " warn" : ""}${item.highlight ? " highlight" : ""}`;
        const name = document.createElement("span");
        name.className = "aura-item-name";
        name.textContent = item.item || "Detail";
        const value = document.createElement("span");
        value.className = "aura-item-val";
        value.textContent = item.amount || "";
        row.append(name, value);
        breakdown.append(row);
      });
      const footer = document.createElement("div");
      footer.className = "aura-hud-footer";
      const recommendation = document.createElement("span");
      recommendation.className = "aura-hud-rec";
      recommendation.textContent = data.action_recommendation || "Review the full context.";
      const mode = document.createElement("span");
      mode.className = "aura-hud-latency";
      mode.textContent = data.analysis_mode === "OPENAI" ? "OpenAI" : "Demo";
      footer.append(recommendation, mode);
      const save = document.createElement("button");
      save.type = "button";
      save.className = "aura-hud-save";
      save.textContent = "Save to Rewind";
      save.addEventListener("click", () => {
        save.disabled = true;
        chrome.runtime.sendMessage({
          type: "SAVE_TO_REWIND",
          title: data.title || "SmartPoint note",
          url: this.lastPageUrl || location.href,
          snippet: `${data.summary || ""}\n\nSelected: ${this.lastSnippet || ""}`.slice(0, 1000)
        }, (res) => {
          save.textContent = res && res.success ? "Saved to Rewind" : "Save failed";
        });
      });
      this.hudElement.append(header, title, summary, breakdown, footer, save);
    }

    document.body.appendChild(this.hudElement);
  }

  showErrorHUD(x, y, errorMsg) {
    this.removeHUD();
    this.hudElement = document.createElement("div");
    this.hudElement.className = "aura-smartpoint-hud";
    this.hudElement.style.width = `${Math.min(360, window.innerWidth - 24)}px`;
    this.hudElement.style.left = `${Math.max(8, Math.min(x, window.innerWidth - 368))}px`;
    this.hudElement.style.top = `${y}px`;
    const header = document.createElement("div");
    header.className = "aura-hud-header";
    const badge = document.createElement("span");
    badge.className = "aura-badge bad";
    badge.textContent = "Analysis unavailable";
    const close = document.createElement("button");
    close.type = "button";
    close.className = "aura-hud-close";
    close.setAttribute("aria-label", "Close SmartPoint");
    close.textContent = "×";
    close.addEventListener("click", () => this.removeHUD());
    header.append(badge, close);
    const message = document.createElement("p");
    message.className = "aura-hud-summary";
    message.textContent = errorMsg || "Start the local AuraOS backend and try again.";
    this.hudElement.append(header, message);
    document.body.appendChild(this.hudElement);
  }

  removeHUD() {
    if (this.hudElement && this.hudElement.parentNode) {
      this.hudElement.parentNode.removeChild(this.hudElement);
      this.hudElement = null;
    }
  }
}

window.auraSmartPoint = new SmartPointEngine();
