# intent_tracker.py
class IntentTracker:
    def __init__(self):
        self.intents = {}

    def set_intent(self, agent_id, intent):
        self.intents[agent_id] = intent

    def get_intent(self, agent_id):
        return self.intents.get(agent_id, "Unknown Intent")
