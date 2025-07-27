# drift_detector.py
class MemoryDriftScanner:
    def __init__(self, baseline_memory, current_memory):
        self.baseline = baseline_memory
        self.current = current_memory

    def scan(self):
        drift_report = []
        for key in self.baseline:
            if key in self.current and self.baseline[key] != self.current[key]:
                drift_report.append(f" Drift on '{key}': {self.baseline[key]} -> {self.current[key]}")
        return drift_report
