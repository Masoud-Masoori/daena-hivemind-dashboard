# long_term_recall_guard.py

class LongTermRecallGuard:
    def __init__(self):
        self.memory_bank = {}

    def save_fact(self, key, fact):
        self.memory_bank[key] = fact

    def retrieve_fact(self, key):
        return self.memory_bank.get(key, "Recall not found")
