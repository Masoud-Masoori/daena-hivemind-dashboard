# feedback_loop_watcher.py
class FeedbackLoopWatcher:
    def __init__(self):
        self.loop_log = []

    def register_response(self, input_text, response_text):
        self.loop_log.append({"in": input_text, "out": response_text})

    def detect_redundancy(self):
        if len(self.loop_log) < 3:
            return False
        return self.loop_log[-1]["out"] == self.loop_log[-2]["out"]
