class InterruptionRecovery:
    def __init__(self):
        self.last_checkpoint = None

    def save_checkpoint(self, state):
        self.last_checkpoint = state

    def recover(self):
        print(" Recovering to checkpoint:", self.last_checkpoint)
        return self.last_checkpoint
