# semantic_watchdog.py
class SemanticWatchdog:
    def __init__(self):
        self.violations = []

    def analyze(self, message):
        if "kill" in message.lower():
            self.violations.append(message)
            return False
        return True

    def report(self):
        return self.violations
