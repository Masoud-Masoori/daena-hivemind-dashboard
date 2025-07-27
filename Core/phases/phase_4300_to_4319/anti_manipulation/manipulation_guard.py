# manipulation_guard.py
class ManipulationGuard:
    def __init__(self, heuristics):
        self.heuristics = heuristics

    def detect(self, message):
        for h in self.heuristics:
            if h in message.lower():
                return True
        return False
