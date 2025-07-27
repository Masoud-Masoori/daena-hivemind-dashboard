# memory_bus.py

global_memory = {}

def update_memory(agent_id, key, value):
    if agent_id not in global_memory:
        global_memory[agent_id] = {}
    global_memory[agent_id][key] = value
    print(f"[MemoryBus]  Updated '{key}' for agent '{agent_id}'.")

def get_memory(agent_id):
    return global_memory.get(agent_id, {})
