### File: core/telemetry/telemetry_sync.py

import json, os
from datetime import datetime

AGENT_STATUS_DIR = "D:/Ideas/Daena/agents"
SYNC_LOG = "D:/Ideas/Daena/logs/telemetry_log.json"

def sync_telemetry():
    status = {}
    for agent in os.listdir(AGENT_STATUS_DIR):
        path = os.path.join(AGENT_STATUS_DIR, agent, "status.json")
        if os.path.exists(path):
            with open(path) as f:
                status[agent] = json.load(f)
    with open(SYNC_LOG, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "telemetry": status
        }, f, indent=2)
    print(f"[TelemetrySync]  Synced {len(status)} agents.")
