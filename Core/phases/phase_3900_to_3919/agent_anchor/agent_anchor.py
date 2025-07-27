# agent_anchor.py
class AgentAnchor:
    def __init__(self):
        self.current_phase = None
        self.checkpoints = {}

    def update_checkpoint(self, agent_id, phase):
        self.checkpoints[agent_id] = phase

    def get_checkpoint(self, agent_id):
        return self.checkpoints.get(agent_id, self.current_phase)

    def restore(self, agent_id):
        return self.get_checkpoint(agent_id)
