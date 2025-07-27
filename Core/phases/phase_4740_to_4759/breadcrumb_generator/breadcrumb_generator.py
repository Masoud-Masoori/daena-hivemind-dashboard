# breadcrumb_generator.py
import time

class BreadcrumbGenerator:
    def __init__(self):
        self.trail = []

    def log_step(self, action, details):
        self.trail.append({
            "timestamp": time.time(),
            "action": action,
            "details": details
        })

    def get_trail(self):
        return self.trail
