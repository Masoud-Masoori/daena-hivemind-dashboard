# inferred_memory_amplifier.py

class InferredMemoryAmplifier:
    def __init__(self):
        self.subtle_patterns = {}

    def absorb(self, user_id, concept):
        if user_id not in self.subtle_patterns:
            self.subtle_patterns[user_id] = []
        self.subtle_patterns[user_id].append(concept)

    def amplify(self, user_id):
        return self.subtle_patterns.get(user_id, [])[-3:]  # Latest 3 patterns
