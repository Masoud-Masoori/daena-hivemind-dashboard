# override_logger.py
from datetime import datetime

def log_override(user, reason):
    entry = {
        "user": user,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }
    with open("D:/Ideas/Daena/core/logs/override_logs.json", "a") as f:
        f.write(str(entry) + "\n")
