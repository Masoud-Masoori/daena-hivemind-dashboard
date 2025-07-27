# intent_tracker.py
class IntentTracker:
    def __init__(self):
        self.intent_log = []

    def register_intent(self, task_id, description):
        self.intent_log.append({"task_id": task_id, "description": description})

    def get_active_intents(self):
        return self.intent_log[-10:]
