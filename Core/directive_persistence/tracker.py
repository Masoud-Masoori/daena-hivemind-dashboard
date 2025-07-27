import json
import os

TRACKER_FILE = "directive_log.json"

def save_directive(directive):
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []
    history.append(directive)
    with open(TRACKER_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_directives():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return []
