# hive_priority_coordinator.py

class HivePriorityCoordinator:
    def __init__(self):
        self.priority_map = {}

    def update_priority(self, agent, priority):
        self.priority_map[agent] = priority

    def get_top_priority(self):
        return sorted(self.priority_map.items(), key=lambda x: x[1], reverse=True)
