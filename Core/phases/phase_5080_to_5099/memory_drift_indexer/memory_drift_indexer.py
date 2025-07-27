# memory_drift_indexer.py
import json

class DriftIndexer:
    def __init__(self):
        self.memory_snapshots = {}

    def snapshot(self, agent_id, memory_dict):
        self.memory_snapshots[agent_id] = memory_dict.copy()

    def detect_drift(self, agent_id, new_memory):
        drift = []
        original = self.memory_snapshots.get(agent_id, {})
        for key, val in new_memory.items():
            if key in original and original[key] != val:
                drift.append((key, original[key], val))
        return drift
