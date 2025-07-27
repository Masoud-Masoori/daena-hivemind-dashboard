# core_stability_lock.py
class CoreStabilityLock:
    def __init__(self):
        self.last_decision = None

    def lock(self, decision_hash):
        self.last_decision = decision_hash

    def is_conflict(self, new_hash):
        return self.last_decision == new_hash
