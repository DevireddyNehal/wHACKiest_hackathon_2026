/**
 * AuraOS Background Service Worker (Manifest V3)
 * Orchestrates communication between Content Scripts, SidePanel, and Backend.
 */

const BACKEND_URL = "http://127.0.0.1:8000";

// Open Side Panel on Extension icon click
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error("SidePanel open error:", error));

// Hotkey listener (Command+Shift+Space or Ctrl+Shift+Space)
chrome.commands.onCommand.addListener((command) => {
  if (command === "toggle-smartpoint") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, { type: "TRIGGER_SMARTPOINT" });
      }
    });
  }
});

// Message relay router
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CHECK_BACKEND_HEALTH") {
    fetch(`${BACKEND_URL}/health`)
      .then((res) => res.json())
      .then((data) => sendResponse({ status: "ONLINE", data }))
      .catch((err) => sendResponse({ status: "OFFLINE", error: err.message }));
    return true; // Keep message channel open for async response
  }

  if (message.type === "ANALYZE_MICRO_DOM") {
    fetch(`${BACKEND_URL}/api/smartpoint/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dom_snippet: message.dom_snippet,
        user_prompt: message.prompt || "Explain and audit this element"
      })
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) {
          throw new Error(typeof data.detail === "string" ? data.detail : "Analysis request failed.");
        }
        return data;
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }
});
