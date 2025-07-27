# fallback_recovery.py
class FallbackRecoveryBrain:
    def __init__(self):
        self.fallbacks = {}

    def save_state(self, agent_id, state_data):
        self.fallbacks[agent_id] = state_data

    def restore_state(self, agent_id):
        return self.fallbacks.get(agent_id, {})
