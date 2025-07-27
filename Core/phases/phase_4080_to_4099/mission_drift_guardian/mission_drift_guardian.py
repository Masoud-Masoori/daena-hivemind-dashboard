# mission_drift_guardian.py
class MissionDriftGuardian:
    def __init__(self, core_objectives):
        self.core_objectives = core_objectives
        self.activity_log = []

    def track_activity(self, action):
        self.activity_log.append(action)

    def is_drifting(self):
        recent = self.activity_log[-5:]
        return not any(obj in str(recent) for obj in self.core_objectives)
