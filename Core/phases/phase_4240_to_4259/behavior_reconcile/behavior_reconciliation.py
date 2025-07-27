# behavior_reconciliation.py
class BehaviorReconciliation:
    def __init__(self, current_behavior, archived_behavior):
        self.current = current_behavior
        self.archive = archived_behavior

    def compare(self):
        diffs = []
        for key in self.current:
            if self.current.get(key) != self.archive.get(key):
                diffs.append((key, self.archive.get(key), self.current.get(key)))
        return diffs
