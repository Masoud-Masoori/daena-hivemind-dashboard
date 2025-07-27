# intention_recovery.py
class IntentionRecovery:
    def __init__(self, anchor):
        self.anchor = anchor

    def detect_divergence(self, current_task, roadmap_task):
        return current_task != roadmap_task

    def recover(self, agent_id, roadmap):
        checkpoint = self.anchor.get_checkpoint(agent_id)
        return roadmap.get(checkpoint, "default_reentry")
