# thought_redundancy_filter.py
class ThoughtRedundancyFilter:
    def __init__(self):
        self.recent_responses = []

    def is_redundant(self, response):
        if response in self.recent_responses[-5:]:
            return True
        self.recent_responses.append(response)
        return False
