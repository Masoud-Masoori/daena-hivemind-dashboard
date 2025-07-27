# reset_resume_coordinator.py

agent_state = {}

def checkpoint(agent_id, state):
    agent_state[agent_id] = state
    print(f"[CHECKPOINT] {agent_id}  {state}")

def restore(agent_id):
    return agent_state.get(agent_id, None)

def clear_checkpoint(agent_id):
    agent_state.pop(agent_id, None)
