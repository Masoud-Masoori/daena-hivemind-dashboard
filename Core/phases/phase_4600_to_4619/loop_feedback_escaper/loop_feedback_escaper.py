# loop_feedback_escaper.py
class LoopFeedbackEscaper:
    def __init__(self, history_limit=5):
        self.history = []

    def record(self, msg):
        self.history.append(msg)
        if len(self.history) > 5:
            self.history.pop(0)

    def detect_loop(self):
        return len(set(self.history)) < len(self.history)
