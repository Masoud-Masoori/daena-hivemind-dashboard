# behavioral_map.py
class BehavioralMap:
    def __init__(self):
        self.behaviors = {}

    def log_behavior(self, agent, context, decision, notes=""):
        if agent not in self.behaviors:
            self.behaviors[agent] = []
        self.behaviors[agent].append({
            "context": context,
            "decision": decision,
            "notes": notes
        })

    def get_map(self, agent):
        return self.behaviors.get(agent, [])
