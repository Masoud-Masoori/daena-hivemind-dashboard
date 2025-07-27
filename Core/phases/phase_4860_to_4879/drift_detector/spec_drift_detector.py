# spec_drift_detector.py
class SpecDriftDetector:
    def __init__(self, baseline):
        self.baseline = baseline

    def detect_drift(self, current_behavior):
        drift_detected = self.baseline != current_behavior
        return drift_detected, {"expected": self.baseline, "actual": current_behavior}
