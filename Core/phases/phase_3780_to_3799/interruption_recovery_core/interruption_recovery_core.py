# interruption_recovery_core.py
import json
import os

class InterruptionRecoveryCore:
    def __init__(self, memory_file="recovery_state.json"):
        self.memory_file = memory_file

    def save_state(self, data):
        with open(self.memory_file, "w") as f:
            json.dump(data, f)

    def load_state(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return {}
