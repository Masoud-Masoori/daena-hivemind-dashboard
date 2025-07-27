# fast_recall_engine.py
class FastRecallEngine:
    def __init__(self, indexer):
        self.indexer = indexer

    def recall_latest(self, n=5):
        return self.indexer.index[-n:]

    def recall_by_topic(self, topic):
        return self.indexer.search(topic)
