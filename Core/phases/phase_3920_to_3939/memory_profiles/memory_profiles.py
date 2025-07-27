# memory_profiles.py
class MemoryProfile:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.short_term = []
        self.long_term = []

    def remember(self, data, long_term=False):
        if long_term:
            self.long_term.append(data)
        else:
            self.short_term.append(data)

    def retrieve(self, term="short"):
        return self.long_term if term == "long" else self.short_term
