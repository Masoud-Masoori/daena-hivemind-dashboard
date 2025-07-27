def failover_check(agent_status):
    if agent_status.get("heartbeat") is False:
        print(f" Agent failed: triggering failover.")
        return True
    return False
