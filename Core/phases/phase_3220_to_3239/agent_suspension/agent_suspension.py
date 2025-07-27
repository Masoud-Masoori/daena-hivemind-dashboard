# agent_suspension.py

suspended_agents = set()

def suspend_agent(agent_id):
    suspended_agents.add(agent_id)
    print(f"[SUSPENSION] Agent '{agent_id}' is now inactive.")

def restore_agent(agent_id):
    suspended_agents.discard(agent_id)
    print(f"[RESTORE] Agent '{agent_id}' has been reactivated.")

def is_suspended(agent_id):
    return agent_id in suspended_agents
