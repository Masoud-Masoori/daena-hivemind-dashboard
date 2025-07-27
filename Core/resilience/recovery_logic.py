class RecoveryLogic:
    def __init__(self):
        self.checkpoints = []

    def save_checkpoint(self, label, context):
        self.checkpoints.append((label, context))
        print(f" Saved checkpoint: {label}")

    def restore_last(self):
        if self.checkpoints:
            last = self.checkpoints[-1]
            print(f" Restoring: {last[0]}")
            return last[1]
        print(" No checkpoints to restore.")
        return None
