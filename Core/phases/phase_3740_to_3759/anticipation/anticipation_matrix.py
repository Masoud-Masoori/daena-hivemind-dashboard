# anticipation_matrix.py
class AnticipationMatrix:
    def __init__(self):
        self.patterns = {}

    def feed(self, context):
        key = context[-1] if context else "none"
        self.patterns[key] = self.patterns.get(key, 0) + 1

    def predict_next(self):
        return max(self.patterns, key=self.patterns.get)
