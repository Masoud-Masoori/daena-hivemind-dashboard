# agent_path_memory.py

agent_paths = {}

def remember_path(agent_id, checkpoint):
    if agent_id not in agent_paths:
        agent_paths[agent_id] = []
    agent_paths[agent_id].append(checkpoint)
    print(f"[NAVIGATION MEMORY] {agent_id} -> {checkpoint}")

def get_path(agent_id):
    return agent_paths.get(agent_id, [])
