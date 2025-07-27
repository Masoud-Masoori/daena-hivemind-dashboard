def attempt_auto_repair(agent_id, issue_type):
    print(f"[RECOVERY] Agent {agent_id} attempting to fix: {issue_type}")
    if issue_type == "timeout":
        return "retrying"
    elif issue_type == "crash":
        return "restart"
    return "manual"
