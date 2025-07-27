# conflict_resolver.py
class ConflictResolver:
    def __init__(self):
        self.votes = {}

    def propose(self, agent, decision):
        self.votes[agent] = decision

    def resolve(self):
        if not self.votes:
            return "No decisions proposed."
        result = max(set(self.votes.values()), key=list(self.votes.values()).count)
        return f"Resolved decision: {result}"
