# swarm_runtime_sync.py
import json
import os

class SwarmSync:
    def __init__(self, sync_file="D:/Ideas/Daena/hive/sync_state.json"):
        self.sync_file = sync_file

    def broadcast_state(self, agent_id, state_data):
        with open(self.sync_file, "w") as f:
            json.dump({"agent": agent_id, "state": state_data}, f)
        print(f"[SwarmSync] Broadcasted {agent_id} state.")

    def get_last_state(self):
        if os.path.exists(self.sync_file):
            with open(self.sync_file, "r") as f:
                return json.load(f)
        return {}
