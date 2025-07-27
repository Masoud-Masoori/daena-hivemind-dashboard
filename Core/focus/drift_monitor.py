class DriftMonitor:
    def __init__(self):
        self.drift_log = []

    def detect(self, current_vector, target_vector):
        if current_vector != target_vector:
            msg = f"Drift Detected: {current_vector} vs {target_vector}"
            self.drift_log.append(msg)
            print(" " + msg)
            return True
        print(" No drift.")
        return False
