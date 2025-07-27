import json
import time

SNAPSHOT_FILE = "D:/Ideas/Daena/data/snapshots/memory_snapshot.json"

def save_snapshot(memory_state):
    snapshot = {
        "timestamp": time.time(),
        "memory": memory_state
    }
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshot, f)
    print("Snapshot saved.")
