# zero_shot_recall_filter.py
class ZeroShotRecallFilter:
    def __init__(self, indexer):
        self.indexer = indexer

    def filter(self, intent):
        # crude zero-shot mimic using keyword match (mock)
        return [e for e in self.indexer.index if intent.lower() in e["text"].lower()]
