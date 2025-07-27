class IntentEchoLogger:
    def __init__(self):
        self.history = []

    def log(self, intent):
        print(f" Echoed Intent: {intent}")
        self.history.append(intent)

    def last_intent(self):
        return self.history[-1] if self.history else None
