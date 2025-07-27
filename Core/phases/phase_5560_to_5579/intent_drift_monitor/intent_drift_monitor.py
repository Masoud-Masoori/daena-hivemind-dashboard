# intent_drift_monitor.py

class IntentDriftMonitor:
    def __init__(self):
        self.intent_history = []

    def record_intent(self, intent_label):
        self.intent_history.append(intent_label)

    def detect_drift(self):
        return len(set(self.intent_history[-5:])) > 2
