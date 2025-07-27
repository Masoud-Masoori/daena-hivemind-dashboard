import traceback
import datetime
import os

LOG_FILE = os.path.join("logs", "telemetry.log")

def secure_log(message, source="unknown"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{source}] {message}\n")

def trace_error(e, source="unknown"):
    stack = traceback.format_exc()
    secure_log(f"ERROR: {e}\\nSTACK: {stack}", source)
