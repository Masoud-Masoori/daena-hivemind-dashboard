class SentinelCheckpoint:
    def __init__(self):
        self.history = []

    def log_decision(self, action):
        self.history.append(action)
        print(f" Checkpointed: {action}")

    def rollback(self, steps=1):
        if steps <= len(self.history):
            print(f" Rolling back {steps} steps.")
            return self.history[:-steps]
        return []
