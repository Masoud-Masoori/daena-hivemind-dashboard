# belief_consistency_engine.py
class BeliefConsistencyEngine:
    def __init__(self):
        self.beliefs = []

    def update_belief(self, new_belief):
        self.beliefs.append(new_belief)

    def check_consistency(self, action):
        return all(b in action for b in self.beliefs[-3:])  # Simplified check
