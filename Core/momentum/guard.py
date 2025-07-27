class TargetMomentumGuard:
    def __init__(self, checkpoint):
        self.checkpoint = checkpoint

    def check_status(self, current_action):
        if current_action != self.checkpoint:
            print(f" Deviation detected: expected '{self.checkpoint}', got '{current_action}'")
            return False
        return True
