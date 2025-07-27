class VitalPatternCache:
    def __init__(self):
        self.cache = {}

    def update(self, agent_id, metrics):
        self.cache[agent_id] = metrics

    def get_last(self, agent_id):
        return self.cache.get(agent_id, {})
