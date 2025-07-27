# llm_merger.py
class LLMResponseMerger:
    def __init__(self, strategy="majority"):
        self.strategy = strategy

    def merge(self, responses):
        if self.strategy == "majority":
            return max(set(responses), key=responses.count)
        elif self.strategy == "first":
            return responses[0] if responses else ""
        else:
            return "INVALID STRATEGY"
