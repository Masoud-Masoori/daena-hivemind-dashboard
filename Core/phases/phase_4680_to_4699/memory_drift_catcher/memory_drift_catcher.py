# memory_drift_catcher.py
class MemoryDriftCatcher:
    def __init__(self):
        self.prev_state = {}

    def detect_drift(self, current_memory):
        drift = {}
        for key, value in current_memory.items():
            if key in self.prev_state and self.prev_state[key] != value:
                drift[key] = (self.prev_state[key], value)
        self.prev_state = current_memory.copy()
        return drift
