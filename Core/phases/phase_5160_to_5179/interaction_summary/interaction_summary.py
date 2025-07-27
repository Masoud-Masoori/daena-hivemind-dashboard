# interaction_summary.py
class InteractionSummary:
    def __init__(self):
        self.messages = []

    def add(self, role, message):
        self.messages.append((role, message))

    def summarize(self):
        return " | ".join([f"{role}: {msg[:20]}..." for role, msg in self.messages[-5:]])
