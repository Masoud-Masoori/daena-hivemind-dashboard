# memory_decay.py
import time

class MemoryDecay:
    def __init__(self, decay_interval_seconds=3600):
        self.memory = {}
        self.last_updated = {}
        self.decay_interval = decay_interval_seconds

    def store(self, key, value):
        self.memory[key] = value
        self.last_updated[key] = time.time()

    def get(self, key):
        now = time.time()
        if key in self.memory and now - self.last_updated[key] < self.decay_interval:
            return self.memory[key]
        return None  # Decayed
