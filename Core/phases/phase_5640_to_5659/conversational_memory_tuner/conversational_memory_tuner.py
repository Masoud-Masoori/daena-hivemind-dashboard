# conversational_memory_tuner.py

class ConversationalMemoryTuner:
    def __init__(self):
        self.conversation_store = []

    def log_interaction(self, user_input, agent_response):
        self.conversation_store.append((user_input, agent_response))

    def tune_memory(self, tuning_keyword):
        return [entry for entry in self.conversation_store if tuning_keyword in entry[0]]
