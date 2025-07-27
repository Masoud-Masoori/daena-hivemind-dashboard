# semantic_drift_detector.py
from difflib import SequenceMatcher

class SemanticDriftDetector:
    def __init__(self, threshold=0.65):
        self.history = []
        self.threshold = threshold

    def add_reference(self, text):
        self.history.append(text)

    def is_drifted(self, current_text):
        if not self.history:
            return False
        similarity = SequenceMatcher(None, self.history[-1], current_text).ratio()
        return similarity < self.threshold
