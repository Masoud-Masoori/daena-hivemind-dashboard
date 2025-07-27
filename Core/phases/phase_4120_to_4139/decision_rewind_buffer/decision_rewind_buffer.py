# decision_rewind_buffer.py
class DecisionRewindBuffer:
    def __init__(self):
        self.checkpoints = []

    def save_checkpoint(self, context_snapshot):
        self.checkpoints.append(context_snapshot)

    def rewind(self):
        return self.checkpoints.pop() if self.checkpoints else None
