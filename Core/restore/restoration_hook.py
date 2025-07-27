class RestorationHook:
    def __init__(self, checkpoints):
        self.checkpoints = checkpoints

    def restore(self, index):
        if index < len(self.checkpoints):
            print(f" Restoring to checkpoint {index}")
            return self.checkpoints[index]
        return None
