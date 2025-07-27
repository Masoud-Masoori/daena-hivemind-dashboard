class DriftAlert:
    def __init__(self):
        self.baseline = None

    def set_baseline(self, phase):
        self.baseline = phase

    def check(self, current):
        if current != self.baseline:
            print(f" Drift detected! Baseline: {self.baseline}, Current: {current}")
            return True
        return False
