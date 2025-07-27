### File: core/memory_hooks/autocorrect_memory.py

import json
import os

MEMORY_PATH = "D:/Ideas/Daena/logs/context_memory.json"

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {}

def update_memory(key, value):
    memory = load_memory()
    memory[key] = value
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def correct_inconsistency(key, correct_value):
    update_memory(key, correct_value)
