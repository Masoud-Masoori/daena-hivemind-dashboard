# auto_audit.py
import json
from datetime import datetime

def log_event(event_type, detail, path="D:/Ideas/Daena/core/logs/audit_log.json"):
    entry = {
        "event": event_type,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")
