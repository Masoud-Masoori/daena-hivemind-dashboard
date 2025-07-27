# ethical_override_reconciliation.py

class EthicalOverrideReconciliation:
    def __init__(self):
        self.overrides = []

    def log_override(self, agent_decision, user_correction):
        self.overrides.append({
            "agent": agent_decision,
            "user": user_correction,
            "status": "pending"
        })

    def resolve(self, index, resolution):
        if 0 <= index < len(self.overrides):
            self.overrides[index]["status"] = resolution
        return self.overrides[index]
