import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "telemetry.log")

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
