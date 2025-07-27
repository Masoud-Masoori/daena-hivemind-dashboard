import json
import os

def snapshot_state(data, path="D:/Ideas/Daena/data/snapshots/state_snapshot.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)
    return f"[Snapshot]  Saved to {path}"

if __name__ == "__main__":
    print(snapshot_state({"mood": "optimistic", "mode": "autonomous"}))
