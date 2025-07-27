class ThreatMirror:
    def __init__(self):
        self.last_reflection = ""

    def reflect(self, threat_signal):
        self.last_reflection = f"REFLECTED::{threat_signal}"
        return self.last_reflection
