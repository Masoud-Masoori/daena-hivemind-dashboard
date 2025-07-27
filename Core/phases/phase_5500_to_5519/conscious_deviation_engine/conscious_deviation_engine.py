# conscious_deviation_engine.py

class ConsciousDeviationEngine:
    def __init__(self, baseline_behavior):
        self.baseline = baseline_behavior

    def deviate(self, context_signal):
        return f"Deviation from {self.baseline} due to context: {context_signal}"
