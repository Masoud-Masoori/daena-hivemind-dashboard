# resource_reallocator.py
import random

class ResourceReallocator:
    def __init__(self):
        self.agent_resources = {}

    def evaluate_usage(self, agent_id, cpu_usage, ram_usage):
        if cpu_usage > 80 or ram_usage > 80:
            return self.reallocate(agent_id)
        return "Stable"

    def reallocate(self, agent_id):
        new_alloc = {"cpu": random.randint(1, 4), "ram": random.randint(1, 8)}
        self.agent_resources[agent_id] = new_alloc
        return f"Reallocated for {agent_id}: CPU {new_alloc['cpu']} cores, RAM {new_alloc['ram']} GB"
