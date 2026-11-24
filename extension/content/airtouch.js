/**
 * AuraOS Pillar 2: AirTouch (Air Mode)
 * User-controlled pointer simulation for the AirTouch demo.
 */

class AirTouchEngine {
  constructor() {
    this.isActive = false;
    this.laserPointer = null;
    this.currentPointedElement = null;
    this.videoElement = null;
    this.smoothedX = window.innerWidth / 2;
    this.smoothedY = window.innerHeight / 2;
    this.initElements();
    console.log("✓ AuraOS AirTouch (Air Mode) registered");
  }

  initElements() {
    // Create virtual laser dot
    this.laserPointer = document.createElement("div");
    this.laserPointer.className = "aura-laser-dot";
    this.laserPointer.style.display = "none";
    document.body.appendChild(this.laserPointer);
  }

  toggleMode(active) {
    this.isActive = active;
    if (this.isActive) {
      this.laserPointer.style.display = "block";
      this.startTracking();
      console.log("🚀 AirTouch Air Mode ENABLED");
    } else {
      this.laserPointer.style.display = "none";
      this.stopTracking();
      console.log("AirTouch Air Mode DISABLED");
    }
  }

  startTracking() {
    // Listens to coordinate streams or simulated spatial pointer
    window.addEventListener("mousemove", this.handlePointerMove);
  }

  stopTracking() {
    window.removeEventListener("mousemove", this.handlePointerMove);
  }

  handlePointerMove = (e) => {
    if (!this.isActive) return;
    this.updateLaser(e.clientX, e.clientY);
  };

  updateLaser(clientX, clientY) {
    // Exponential smoothing
    this.smoothedX = this.smoothedX * 0.7 + clientX * 0.3;
    this.smoothedY = this.smoothedY * 0.7 + clientY * 0.3;

    this.laserPointer.style.left = `${this.smoothedX}px`;
    this.laserPointer.style.top = `${this.smoothedY}px`;

    // Spatial raycasting: find target element under laser
    this.laserPointer.style.pointerEvents = "none";
    const target = document.elementFromPoint(this.smoothedX, this.smoothedY);
    if (target && target !== this.currentPointedElement) {
      if (this.currentPointedElement) {
        this.currentPointedElement.classList.remove("aura-laser-focus");
      }
      this.currentPointedElement = target.closest("button, a, input, [role='button'], .card") || target;
      if (this.currentPointedElement) {
        this.currentPointedElement.classList.add("aura-laser-focus");
      }
    }
  }

  // Simulated Pinch Gesture (Triggers synthetic click)
  triggerPinchClick() {
    if (this.currentPointedElement) {
      this.laserPointer.classList.add("pinch-pulse");
      setTimeout(() => this.laserPointer.classList.remove("pinch-pulse"), 400);
      this.currentPointedElement.click();
      console.log("Pinch click executed on:", this.currentPointedElement);
    }
  }

  // Simulated Palm Swipe (Triggers smooth scroll)
  triggerScroll(direction) {
    const delta = direction === "UP" ? -350 : 350;
    window.scrollBy({ top: delta, behavior: "smooth" });
  }
}

window.auraAirTouch = new AirTouchEngine();
