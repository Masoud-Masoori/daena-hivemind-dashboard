# agent_state_locker.py
import json
import os

class StateLocker:
    def __init__(self, state_dir="D:/Ideas/Daena/core/state"):
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)

    def lock(self, agent_id, state_data):
        with open(f"{self.state_dir}/{agent_id}_state.json", "w") as f:
            json.dump(state_data, f)

    def unlock(self, agent_id):
        try:
            with open(f"{self.state_dir}/{agent_id}_state.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
