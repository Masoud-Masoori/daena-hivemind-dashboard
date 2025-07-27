# accountability_pipeline.py
import json, os

class AccountabilityPipeline:
    def __init__(self, log_path="D:/Ideas/Daena/logs/mission_flow.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log_action(self, agent_id, action, phase):
        record = {
            "agent_id": agent_id,
            "action": action,
            "phase": phase
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(record) + "\n")
