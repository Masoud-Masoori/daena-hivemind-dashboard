class MissionDriftWatcher:
    def __init__(self, baseline):
        self.baseline = baseline

    def detect_drift(self, current_goal):
        if current_goal != self.baseline:
            print(" Drift detected! Returning to baseline.")
            return True
        return False
