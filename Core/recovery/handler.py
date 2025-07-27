class PivotRecovery:
    def __init__(self):
        self.interrupted_phase = None

    def record_pivot(self, phase):
        self.interrupted_phase = phase

    def resume(self):
        if self.interrupted_phase:
            print(f" Resuming from pivot at: {self.interrupted_phase}")
            return self.interrupted_phase
