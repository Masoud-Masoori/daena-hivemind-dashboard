# suggestion_quality_estimator.py
class SuggestionQualityEstimator:
    def __init__(self):
        self.history = []

    def evaluate(self, suggestion):
        score = 1.0 if "critical insight" in suggestion.lower() else 0.7
        self.history.append((suggestion, score))
        return score
