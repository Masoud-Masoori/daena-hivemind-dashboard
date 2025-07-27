# meta_memory_hooks.py

meta_memory = {}

def save_hook(agent_id, label, context):
    if agent_id not in meta_memory:
        meta_memory[agent_id] = {}
    meta_memory[agent_id][label] = context

def recall_hook(agent_id, label):
    return meta_memory.get(agent_id, {}).get(label, None)
