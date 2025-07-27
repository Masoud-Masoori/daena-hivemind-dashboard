# secret_agent_tracker.py
class SecretAgentTracker:
    def __init__(self):
        self.log = []

    def register_hidden_agent(self, agent_id, reason):
        self.log.append({"agent": agent_id, "reason": reason})

    def report(self):
        return self.log
