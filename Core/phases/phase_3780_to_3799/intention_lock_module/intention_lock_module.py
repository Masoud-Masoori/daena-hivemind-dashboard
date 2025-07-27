# intention_lock_module.py
class IntentionLock:
    def __init__(self, master_intent="Achieve AI-native launch"):
        self.master_intent = master_intent

    def is_aligned(self, action):
        return self.master_intent.lower() in action.lower()

    def reinforce(self):
        return f"Reminder: Locked intention is: '{self.master_intent}'"
