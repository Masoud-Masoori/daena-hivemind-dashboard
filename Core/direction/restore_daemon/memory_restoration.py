import os
import json

MEMORY_FILE = "mission_log.json"

def restore_last_known_state():
    if not os.path.exists(MEMORY_FILE):
        return None
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def persist_mission(mission_state):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mission_state, f)
