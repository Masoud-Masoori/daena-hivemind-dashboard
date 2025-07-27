class GlobalPhaseMarker:
    def __init__(self):
        self.current_phase = 0

    def mark(self, phase_number):
        self.current_phase = phase_number
        print(f" Global Phase updated to: {phase_number}")

    def get(self):
        return self.current_phase
