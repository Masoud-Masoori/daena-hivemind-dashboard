# sentiment_map.py

class DistributedSentimentMap:
    def __init__(self):
        self.sentiments = []

    def add_entry(self, source, tone, weight=1):
        self.sentiments.append({"source": source, "tone": tone, "weight": weight})

    def summary(self):
        score = sum(s["weight"] if s["tone"] == "positive" else -s["weight"] for s in self.sentiments)
        return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
