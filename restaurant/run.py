"""One-command launcher for the BBQ BI MVP.

Builds the database if missing and starts the FastAPI backend. Stopping (Ctrl-C) shuts the API down.

    python run.py
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def ensure_db() -> None:
    from app import config

    if not Path(config.DB_PATH).exists():
        print("Database not found — building it from the CSVs…")
        subprocess.run([sys.executable, "scripts/load_data.py"], cwd=ROOT, check=True)


def main() -> None:
    sys.path.insert(0, str(ROOT))
    ensure_db()

    print("Starting API on http://127.0.0.1:8000 …")
    api = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=ROOT,
    )
    try:
        # Streamlit dashboard disabled per request – only FastAPI backend runs
        print("FastAPI backend is running at http://127.0.0.1:8000")
        api.wait()  # keep the script alive while API is running
    finally:
        print("\nShutting down API…")
        api.terminate()
        try:
            api.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api.kill()


if __name__ == "__main__":
    main()
