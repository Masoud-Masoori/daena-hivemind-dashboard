# founder_intent_enforcer.py
class FounderIntentEnforcer:
    def __init__(self, declared_intents):
        self.intents = declared_intents

    def verify(self, action):
        if action not in self.intents["allowed"]:
            return f" Action '{action}' violates founder directives."
        return f" Action '{action}' aligns with Masoud's vision."
