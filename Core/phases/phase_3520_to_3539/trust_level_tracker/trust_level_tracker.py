# trust_level_tracker.py

class TrustLevelTracker:
    def __init__(self):
        self.trust_scores = {}

    def update_trust(self, agent_id, delta):
        current = self.trust_scores.get(agent_id, 0.5)
        self.trust_scores[agent_id] = max(0.0, min(1.0, current + delta))

    def get_trust(self, agent_id):
        return self.trust_scores.get(agent_id, 0.5)
