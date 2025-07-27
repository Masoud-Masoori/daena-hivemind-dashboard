# decision_trailkeeper.py
class DecisionTrailkeeper:
    def __init__(self):
        self.decision_log = {}

    def log_decision(self, agent_id, decision):
        if agent_id not in self.decision_log:
            self.decision_log[agent_id] = []
        self.decision_log[agent_id].append(decision)

    def get_decisions(self, agent_id):
        return self.decision_log.get(agent_id, [])
