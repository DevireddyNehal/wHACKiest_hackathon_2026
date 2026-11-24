"""
AuraOS Root Entrypoint
Delegates execution to the master backend in backend/main.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.main import app
import uvicorn
from backend.config import settings

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
