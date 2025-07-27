# ai_reflector.py
class AIReflector:
    def __init__(self):
        self.past_conversations = []

    def store(self, message):
        self.past_conversations.append(message)
        if len(self.past_conversations) > 100:
            self.past_conversations.pop(0)

    def simulate_reflection(self, query):
        return f"Based on previous experience with '{query}', the optimal approach is likely..."
