# role_recall_engine.py
class RoleRecallEngine:
    def __init__(self):
        self.role_map = {}

    def assign_role(self, agent_id, role):
        self.role_map[agent_id] = role

    def recall(self, agent_id):
        return self.role_map.get(agent_id, "unassigned")
