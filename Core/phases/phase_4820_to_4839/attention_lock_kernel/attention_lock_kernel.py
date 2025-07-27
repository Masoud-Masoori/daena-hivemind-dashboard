# attention_lock_kernel.py
class AttentionLockKernel:
    def __init__(self):
        self.locks = {}

    def lock_focus(self, agent_id, focus_area):
        self.locks[agent_id] = focus_area

    def get_locked_focus(self, agent_id):
        return self.locks.get(agent_id, "No locked focus")
