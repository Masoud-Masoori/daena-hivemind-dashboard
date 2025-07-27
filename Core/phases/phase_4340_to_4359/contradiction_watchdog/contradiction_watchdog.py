# contradiction_watchdog.py
class ContradictionWatchdog:
    def __init__(self):
        self.memory_log = []

    def log(self, statement):
        self.memory_log.append(statement)

    def detect_conflict(self):
        seen = set()
        for stmt in self.memory_log:
            if stmt in seen:
                return True
            seen.add(stmt)
        return False
