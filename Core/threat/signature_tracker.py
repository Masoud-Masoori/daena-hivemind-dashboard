class ThreatSignatureTracker:
    def __init__(self):
        self.signatures = []

    def log(self, signature):
        if signature not in self.signatures:
            self.signatures.append(signature)

    def match(self, incoming):
        return incoming in self.signatures
