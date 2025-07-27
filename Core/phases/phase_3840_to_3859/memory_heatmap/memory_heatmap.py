# memory_heatmap.py
import math
import time

class MemoryHeatMapper:
    def __init__(self):
        self.memory_bank = {}

    def update(self, key):
        timestamp = time.time()
        self.memory_bank[key] = timestamp

    def get_hot_items(self, top_n=5):
        sorted_items = sorted(self.memory_bank.items(), key=lambda x: x[1], reverse=True)
        return [k for k, _ in sorted_items[:top_n]]
