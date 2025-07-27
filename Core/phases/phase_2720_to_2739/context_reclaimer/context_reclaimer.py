# context_reclaimer.py
import json
from datetime import datetime

CONTEXT_FILE = "D:/Ideas/Daena/logs/context_log.json"

def save_context(agent, location, reason):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "location": location,
        "reason": reason
    }
    try:
        with open(CONTEXT_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = []
    data.append(entry)
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"[ContextReclaimer] Saved context snapshot for {agent}")
