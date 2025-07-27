import json

def snapshot_state():
    state = {
        "status": "active",
        "level": "self-monitoring",
        "timestamp": "2025-06-01T00:00:00Z"
    }
    with open("snapshot.json", "w") as snap:
        json.dump(state, snap, indent=2)

if __name__ == "__main__":
    snapshot_state()
    print(" Agent state snapshot saved.")
