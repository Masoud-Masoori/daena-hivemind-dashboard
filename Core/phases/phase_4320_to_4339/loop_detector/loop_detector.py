# loop_detector.py
class LoopDetector:
    def __init__(self):
        self.history = []

    def update(self, message):
        self.history.append(message)
        if len(self.history) > 20:
            self.history.pop(0)

    def is_looping(self):
        return len(set(self.history[-5:])) <= 2
