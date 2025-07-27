class ContinuityKeeper:
    def __init__(self):
        self.current_focus = None
        self.last_checkpoint = None

    def set_focus(self, focus):
        self.current_focus = focus
        print(f" Focus set to: {focus}")

    def checkpoint(self):
        self.last_checkpoint = self.current_focus
        print(f" Checkpoint saved: {self.last_checkpoint}")

    def resume(self):
        if self.last_checkpoint:
            print(f" Resuming from: {self.last_checkpoint}")
            self.current_focus = self.last_checkpoint
