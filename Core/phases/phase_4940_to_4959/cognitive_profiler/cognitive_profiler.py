# cognitive_profiler.py
class CognitiveProfiler:
    def __init__(self):
        self.agent_patterns = {}

    def update_profile(self, agent_name, response_time, logic_depth, creative_score):
        if agent_name not in self.agent_patterns:
            self.agent_patterns[agent_name] = []
        self.agent_patterns[agent_name].append({
            "response_time": response_time,
            "logic_depth": logic_depth,
            "creative_score": creative_score
        })

    def get_profile(self, agent_name):
        return self.agent_patterns.get(agent_name, [])
