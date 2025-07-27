# dashboard_relay_sync.py

import json
import os

def update_dashboard_state(agent, status):
    data = {
        "agent": agent,
        "status": status
    }
    path = os.path.join("D:/Ideas/Daena/live_status", f"{agent}_status.json")
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[Dashboard]  Updated status for {agent}: {status}")
