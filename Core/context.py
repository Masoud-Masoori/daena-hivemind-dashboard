import time

class VoiceContext:
    def __init__(self):
        self.history = []

    def record(self, text):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.history.append((timestamp, text))
        self.history = self.history[-10:]  # Keep only last 10
        return self.history

    def get_last(self):
        return self.history[-1] if self.history else ("", "")
