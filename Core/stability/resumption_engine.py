from core.navigation.checkpoints.checkpoint_resolver import CheckpointResolver

class ResumptionEngine:
    def __init__(self, checkpoint_path):
        self.resolver = CheckpointResolver(checkpoint_path)

    def resume(self):
        last = self.resolver.last_checkpoint()
        if last:
            print(f" Resuming from Phase {last[0]}  {last[1]}")
            return last
        else:
            print(" No previous checkpoints found.")
            return None
