# feedback_rationalizer.py
class FeedbackRationalizer:
    def __init__(self):
        self.history = []

    def integrate(self, feedback_sources):
        combined = " | ".join([f"{src['agent']}: {src['comment']}" for src in feedback_sources])
        self.history.append(combined)
        return combined
