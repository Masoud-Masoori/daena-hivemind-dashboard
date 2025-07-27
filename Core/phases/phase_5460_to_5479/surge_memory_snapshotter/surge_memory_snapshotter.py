# surge_memory_snapshotter.py

import json
import time

class SurgeMemorySnapshotter:
    def __init__(self, path="snapshots.jsonl"):
        self.path = path

    def capture(self, state):
        snapshot = {
            "timestamp": time.time(),
            "state": state
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(snapshot) + "\n")
