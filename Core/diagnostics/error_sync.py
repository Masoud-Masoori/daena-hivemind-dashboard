def sync_errors_to_hive(agent_errors):
    for agent_id, error in agent_errors.items():
        print(f"[SYNC] Agent {agent_id} shared error: {error}")
    return True
