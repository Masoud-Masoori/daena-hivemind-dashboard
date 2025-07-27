# drift_alignment.py
class FeedbackDriftAligner:
    def __init__(self):
        self.feedback_log = []

    def register_feedback(self, agent_id, feedback):
        self.feedback_log.append((agent_id, feedback))

    def detect_drift(self):
        drift_count = sum(1 for _, fb in self.feedback_log[-10:] if "drift" in fb)
        return drift_count > 3
