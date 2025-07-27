# override_layer.py
import time

class EmergencyOverride:
    def __init__(self):
        self.manual_triggered = False
        self.auto_trigger_conditions = []

    def manual_override(self):
        self.manual_triggered = True
        return " Manual override activated."

    def evaluate_conditions(self, system_state):
        for cond in self.auto_trigger_conditions:
            if cond(system_state):
                return " Automatic override triggered."
        return " Normal"
