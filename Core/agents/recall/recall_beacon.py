def beacon_signal(agent_registry, agent_id):
    return agent_registry.get(agent_id, {}).get("last_task", "No recent activity.")
