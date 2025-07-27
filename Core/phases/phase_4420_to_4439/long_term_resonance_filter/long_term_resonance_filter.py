# long_term_resonance_filter.py
import time

class LongTermResonanceFilter:
    def __init__(self):
        self.memory_log = []

    def log_event(self, event, importance):
        self.memory_log.append({
            "timestamp": time.time(),
            "event": event,
            "importance": importance
        })

    def get_resonant_events(self, threshold=0.8):
        return [e for e in self.memory_log if e["importance"] >= threshold]
