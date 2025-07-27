class ResyncBeacon:
    def __init__(self):
        self.reference_pulse = "main_project_objective"

    def emit_beacon(self):
        print(f" Emitting beacon to maintain alignment with: {self.reference_pulse}")

    def check_alignment(self, current_pulse):
        if current_pulse != self.reference_pulse:
            print(" Drift detected! Initiating corrective sync...")
            return False
        print(" Alignment verified.")
        return True
