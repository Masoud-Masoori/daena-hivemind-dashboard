class ReEntryBridge:
    def __init__(self):
        self.checkpoints = []

    def mark_checkpoint(self, label):
        print(f" Checkpoint set: {label}")
        self.checkpoints.append(label)

    def resume_from_last(self):
        if self.checkpoints:
            last = self.checkpoints[-1]
            print(f" Resuming from: {last}")
            return last
        print(" No checkpoints found.")
        return None
