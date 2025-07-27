# directive_drift_anchor.py

class DirectiveDriftAnchor:
    def __init__(self, baseline_mission):
        self.baseline = baseline_mission
        self.current_state = baseline_mission

    def verify_alignment(self, current_mission):
        if current_mission != self.baseline:
            return f" Drift Detected: Return to core directive  {self.baseline}"
        return " Aligned"
