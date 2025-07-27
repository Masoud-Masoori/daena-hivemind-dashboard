# signal_pattern_auditor.py
class SignalPatternAuditor:
    def __init__(self):
        self.pattern_log = []

    def audit(self, signal_sequence):
        # Capture and log the pattern of signals
        compressed = "".join([s[0] for s in signal_sequence])
        self.pattern_log.append(compressed)
        return compressed
