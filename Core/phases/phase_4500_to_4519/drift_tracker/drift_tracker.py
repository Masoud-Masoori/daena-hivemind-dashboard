# drift_tracker.py
import time

class DriftTracker:
    def __init__(self):
        self.start_point = None
        self.current_point = None

    def mark_start(self, tag):
        self.start_point = {"tag": tag, "timestamp": time.time()}

    def update_current(self, tag):
        self.current_point = {"tag": tag, "timestamp": time.time()}

    def detect_drift(self):
        return self.start_point["tag"] != self.current_point["tag"] if self.start_point and self.current_point else False
