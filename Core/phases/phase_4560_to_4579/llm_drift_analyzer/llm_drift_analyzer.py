# llm_drift_analyzer.py
from difflib import SequenceMatcher

class LLMDriftAnalyzer:
    def __init__(self, base_truths):
        self.base_truths = base_truths

    def analyze(self, llm_output):
        similarities = [
            (truth, SequenceMatcher(None, llm_output, truth).ratio())
            for truth in self.base_truths
        ]
        return sorted(similarities, key=lambda x: x[1], reverse=True)
