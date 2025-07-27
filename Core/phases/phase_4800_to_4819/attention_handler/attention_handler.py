# attention_handler.py
class AutonomousAttentionHandler:
    def __init__(self):
        self.agent_focus = {}

    def focus_on(self, agent_id, item):
        self.agent_focus[agent_id] = item

    def get_focus(self, agent_id):
        return self.agent_focus.get(agent_id, "No active focus")
