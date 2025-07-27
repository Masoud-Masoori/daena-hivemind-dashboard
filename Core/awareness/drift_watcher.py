class DriftWatcher:
    def __init__(self, roadmap_status):
        self.roadmap_status = roadmap_status
        self.drift_log = []

    def check_alignment(self, current_focus):
        if current_focus not in self.roadmap_status.get("expected"):
            self.drift_log.append(current_focus)
            print(f" Drift detected: {current_focus}")
            return False
        return True
