class DriftPreventionKernel:
    def __init__(self):
        self.last_verified_phase = None

    def update_phase(self, phase):
        self.last_verified_phase = phase

    def detect_drift(self, current_phase):
        if self.last_verified_phase and abs(current_phase - self.last_verified_phase) > 20:
            print(" Drift detected. System might be off-track.")
            return True
        return False
