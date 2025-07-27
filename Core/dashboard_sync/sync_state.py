### File: core/dashboard_sync/sync_state.py

import json
import os

SYNC_PATH = "D:/Ideas/Daena/logs/dashboard_state.json"

def update_dashboard(agent_state):
    with open(SYNC_PATH, "w") as f:
        json.dump(agent_state, f, indent=2)

def get_current_dashboard_state():
    if os.path.exists(SYNC_PATH):
        with open(SYNC_PATH, "r") as f:
            return json.load(f)
    return {}
