# behavioral_regression_scanner.py
class BehavioralRegressionScanner:
    def __init__(self):
        self.baseline_traits = {"honesty", "curiosity", "focus"}

    def scan(self, traits):
        return any(trait not in self.baseline_traits for trait in traits)
