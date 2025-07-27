def harmonize_agents(agent_statuses):
    consensus = all(status == "ready" for status in agent_statuses)
    return "synchronized" if consensus else "desynced"
