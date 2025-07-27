# closure_bridge.py
import datetime

class ClosureBridge:
    def __init__(self):
        self.history = []

    def mark_complete(self, phase_name):
        self.history.append({
            "phase": phase_name,
            "timestamp": datetime.datetime.now().isoformat()
        })

    def get_closure_log(self):
        return self.history
