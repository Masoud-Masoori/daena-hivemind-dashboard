# command_trail.py

import json
import os
from datetime import datetime

TRAIL_LOG = "D:/Ideas/Daena/logs/command_trail.json"

def log_command(agent, command):
    log = {
        "agent": agent,
        "command": command,
        "time": datetime.now().isoformat()
    }
    try:
        with open(TRAIL_LOG, 'r') as f:
            trail = json.load(f)
    except:
        trail = []

    trail.append(log)
    with open(TRAIL_LOG, 'w') as f:
        json.dump(trail, f, indent=2)
    print(f"[TrailLog] Agent '{agent}' logged command: {command}")
