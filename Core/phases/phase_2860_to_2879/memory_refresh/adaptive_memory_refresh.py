# adaptive_memory_refresh.py

import random

def refresh_memory(memory_bank, urgency_level):
    retention_threshold = max(0.3, 1 - urgency_level * 0.1)
    refreshed = {k: v for k, v in memory_bank.items() if random.random() < retention_threshold}
    print(f"[MemoryRefresh]  Retained {len(refreshed)} of {len(memory_bank)} entries.")
    return refreshed
