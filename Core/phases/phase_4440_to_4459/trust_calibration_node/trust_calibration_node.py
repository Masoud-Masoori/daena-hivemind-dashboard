# trust_calibration_node.py
class TrustCalibrationNode:
    def __init__(self):
        self.trust_scores = {}

    def update_trust(self, agent_id, score_delta):
        self.trust_scores[agent_id] = self.trust_scores.get(agent_id, 0) + score_delta

    def get_trust_level(self, agent_id):
        return self.trust_scores.get(agent_id, 0)
