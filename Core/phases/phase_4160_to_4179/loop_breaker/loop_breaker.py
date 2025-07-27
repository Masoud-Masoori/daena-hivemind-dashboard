# loop_breaker.py
class LoopBreaker:
    def __init__(self):
        self.history = set()

    def detect_and_break(self, signature):
        if signature in self.history:
            return True  # Loop detected
        self.history.add(signature)
        return False
