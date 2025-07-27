# state_freezer.py
import json
import os

STATE_FILE = "D:/Ideas/Daena/logs/state_snapshot.json"

def freeze_state(data):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print("[Freezer] State frozen.")

def load_last_state():
    if not os.path.exists(STATE_FILE):
        print("[Freezer] No previous state found.")
        return None
    with open(STATE_FILE, 'r') as f:
        return json.load(f)
