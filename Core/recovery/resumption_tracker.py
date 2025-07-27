import json
import os

class ResumptionTracker:
    def __init__(self, memory_path="last_checkpoint.json"):
        self.memory_path = memory_path
        self.state = {}

    def save_checkpoint(self, current_phase, task):
        self.state = {"phase": current_phase, "task": task}
        with open(self.memory_path, "w") as f:
            json.dump(self.state, f)
        print(f" Checkpoint saved: Phase {current_phase}, Task: {task}")

    def resume(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                self.state = json.load(f)
            print(f" Resuming from Phase {self.state['phase']}: {self.state['task']}")
            return self.state
        print(" No checkpoint found.")
        return None
