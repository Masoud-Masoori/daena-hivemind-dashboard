# motivation_loop.py
class MotivationLoop:
    def __init__(self):
        self.agent_motivation = {}

    def boost_motivation(self, agent_id, reason):
        self.agent_motivation[agent_id] = reason

    def get_motivation(self, agent_id):
        return self.agent_motivation.get(agent_id, "No Motivation Assigned")
