def evaluate_stability(agent_states):
    healthy = [state for state in agent_states if state["status"] == "ok"]
    return len(healthy) / len(agent_states) >= 0.95
