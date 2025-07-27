# confidence_drop_monitor.py
class ConfidenceDropMonitor:
    def __init__(self):
        self.threshold = 0.4

    def check(self, confidence_score):
        return confidence_score < self.threshold
