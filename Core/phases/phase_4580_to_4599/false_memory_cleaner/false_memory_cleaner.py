# false_memory_cleaner.py
class FalseMemoryCleaner:
    def __init__(self, memory_bank):
        self.memory = memory_bank

    def purge_invalid_entries(self, validator_fn):
        self.memory = [entry for entry in self.memory if validator_fn(entry)]
        return self.memory
