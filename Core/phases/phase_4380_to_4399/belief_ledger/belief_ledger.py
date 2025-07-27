# belief_ledger.py
import datetime

class BeliefLedger:
    def __init__(self):
        self.ledger = []

    def record(self, belief, source="internal", confidence=0.5):
        self.ledger.append({
            "belief": belief,
            "source": source,
            "confidence": confidence,
            "timestamp": datetime.datetime.now().isoformat()
        })

    def get_all(self):
        return self.ledger
