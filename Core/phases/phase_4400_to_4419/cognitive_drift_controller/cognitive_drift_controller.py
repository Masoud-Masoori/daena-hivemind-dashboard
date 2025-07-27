# cognitive_drift_controller.py
class CognitiveDriftController:
    def __init__(self):
        self.history = []

    def register_decision(self, decision):
        self.history.append(decision)
        if len(self.history) > 10:
            self.history.pop(0)

    def detect_drift(self):
        return len(set(self.history[-5:])) == 1
