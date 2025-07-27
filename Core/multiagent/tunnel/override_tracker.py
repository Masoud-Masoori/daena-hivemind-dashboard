class EthicalOverrideTracker:
    def __init__(self):
        self.log = []

    def track(self, reason, agent_id):
        self.log.append({"agent": agent_id, "reason": reason})

    def audit(self):
        return self.log
