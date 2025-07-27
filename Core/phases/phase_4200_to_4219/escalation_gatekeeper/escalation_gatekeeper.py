# escalation_gatekeeper.py
class EscalationGatekeeper:
    def __init__(self):
        self.levels = {"GUEST": 0, "AGENT": 1, "ADMIN": 2, "FOUNDER": 3}

    def request_access(self, current, requested):
        if self.levels.get(requested, -1) > self.levels.get(current, -1):
            return f" Escalation from {current} to {requested} denied."
        return f" Access level {requested} granted."

