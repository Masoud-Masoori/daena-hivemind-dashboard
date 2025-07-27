# bias_reduction_engine.py
import nltk

class BiasReductionEngine:
    def __init__(self):
        self.bias_terms = ["always", "never", "everyone", "no one"]

    def reduce_bias(self, text):
        for term in self.bias_terms:
            text = text.replace(term, f"possibly {term}")
        return text
