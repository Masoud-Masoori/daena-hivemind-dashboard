class ContinuityEnforcer:
    def __init__(self):
        self.active_phase = None

    def register_phase(self, phase):
        self.active_phase = phase

    def verify(self, current_phase):
        if current_phase != self.active_phase:
            print(f"Warning: phase mismatch. Resetting to: {self.active_phase}")
            return self.active_phase
        return current_phase
