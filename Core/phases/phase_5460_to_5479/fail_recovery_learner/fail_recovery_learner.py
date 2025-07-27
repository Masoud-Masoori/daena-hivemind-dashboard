# fail_recovery_learner.py

class FailRecoveryLearner:
    def __init__(self):
        self.failures = []

    def log_failure(self, context, error):
        self.failures.append((context, error))

    def get_recovery_plan(self):
        return "Review previous context and retry with adjustments"
