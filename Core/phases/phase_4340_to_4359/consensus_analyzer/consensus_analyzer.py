# consensus_analyzer.py
class ConsensusAnalyzer:
    def __init__(self):
        self.responses = {}

    def add_response(self, agent, response):
        self.responses[agent] = response

    def majority_vote(self):
        from collections import Counter
        values = list(self.responses.values())
        return Counter(values).most_common(1)[0][0] if values else None
