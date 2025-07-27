# realtime_feedback_listener.py
class RealTimeFeedbackListener:
    def __init__(self):
        self.log = []

    def listen(self, message):
        self.log.append(message)
        return "feedback" in message.lower() or "issue" in message.lower()
