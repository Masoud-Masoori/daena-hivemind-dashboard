# heuristic_tracker.py
class HeuristicTracker:
    def __init__(self):
        self.heuristics_used = {}

    def log_heuristic(self, agent_name, heuristic_type, frequency=1):
        if agent_name not in self.heuristics_used:
            self.heuristics_used[agent_name] = {}
        self.heuristics_used[agent_name][heuristic_type] = self.heuristics_used[agent_name].get(heuristic_type, 0) + frequency

    def get_agent_heuristics(self, agent_name):
        return self.heuristics_used.get(agent_name, {})
