# cause_effect_memory.py
class CauseEffectMemory:
    def __init__(self):
        self.outcomes = []

    def record(self, action, outcome):
        self.outcomes.append((action, outcome))

    def analyze_effects(self):
        return {action: outcome for action, outcome in self.outcomes}
