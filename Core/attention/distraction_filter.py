class DistractionFilter:
    def __init__(self, allowed_keywords=[]):
        self.allowed_keywords = allowed_keywords

    def is_relevant(self, topic):
        return any(kw in topic.lower() for kw in self.allowed_keywords)
