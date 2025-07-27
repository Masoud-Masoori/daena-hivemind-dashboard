# cloud_state_interlinker.py

class CloudStateInterlinker:
    def __init__(self):
        self.linked_agents = {}

    def update_state(self, agent_id, state_data):
        self.linked_agents[agent_id] = state_data

    def get_state(self, agent_id):
        return self.linked_agents.get(agent_id, "No state available")
