/**
 * AuraOS Master Content Script Coordinator
 * Bridges incoming messages from SidePanel/Background to SmartPoint and AirTouch engines.
 */

console.log("🌟 AuraOS Autonomous Web Operating System injected on page:", window.location.href);

// Listen to Mode switches and commands from the SidePanel
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "SET_MODE") {
    const isAirMode = msg.mode === "AIR";
    if (window.auraAirTouch) {
      window.auraAirTouch.toggleMode(isAirMode);
    }
    sendResponse({ status: "MODE_UPDATED", mode: msg.mode });
  }

  if (msg.type === "PINCH_CLICK") {
    if (window.auraAirTouch) {
      window.auraAirTouch.triggerPinchClick();
    }
    sendResponse({ status: "CLICK_TRIGGERED" });
  }

  if (msg.type === "AIR_SCROLL") {
    if (window.auraAirTouch) {
      window.auraAirTouch.triggerScroll(msg.direction || "DOWN");
    }
    sendResponse({ status: "SCROLLED" });
  }
});
