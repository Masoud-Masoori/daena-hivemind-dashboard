# truth_deviation_handler.py
class TruthDeviationHandler:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def check_deviation(self, similarity_score):
        return similarity_score < self.threshold
