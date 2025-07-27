class DistractionRecovery:
    def __init__(self):
        self.events = []

    def record(self, event, resolved=False):
        self.events.append({"event": event, "resolved": resolved})

    def unresolved(self):
        return [e for e in self.events if not e["resolved"]]
