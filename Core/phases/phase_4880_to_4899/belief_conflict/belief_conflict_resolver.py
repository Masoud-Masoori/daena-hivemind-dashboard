# belief_conflict_resolver.py
class BeliefConflictResolver:
    def __init__(self):
        self.conflicts = []

    def resolve(self, beliefs):
        conflicting = [b for b in beliefs if beliefs.count(b) > 1 and beliefs.count(b) % 2 == 0]
        self.conflicts.append(conflicting)
        return list(set(beliefs) - set(conflicting)), conflicting
