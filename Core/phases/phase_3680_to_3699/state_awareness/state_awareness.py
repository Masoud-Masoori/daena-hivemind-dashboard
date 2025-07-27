# state_awareness.py
import time

class StateMonitor:
    def __init__(self):
        self.agent_states = {}

    def update_state(self, agent_id, state):
        self.agent_states[agent_id] = {"state": state, "timestamp": time.time()}

    def get_state(self, agent_id):
        return self.agent_states.get(agent_id, None)

    def list_all(self):
        return self.agent_states
