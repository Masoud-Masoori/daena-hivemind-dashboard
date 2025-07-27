# swarm_reorder.py

def reorganize_swarm(agent_priority_dict):
    sorted_agents = sorted(agent_priority_dict.items(), key=lambda x: x[1])
    print("[REORDERED SWARM]")
    for idx, (agent, priority) in enumerate(sorted_agents):
        print(f"{idx+1}. Agent: {agent}, Priority: {priority}")
    return sorted_agents
