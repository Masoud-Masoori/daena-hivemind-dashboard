# continuity_memory_gate.py
class ContinuityMemoryGate:
    def __init__(self):
        self.last_context = {}

    def save_context(self, agent_id, task_state):
        self.last_context[agent_id] = task_state

    def restore_context(self, agent_id):
        return self.last_context.get(agent_id, None)
