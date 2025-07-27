def monitor_agents(agent_logs, budget_threshold):
    for log in agent_logs:
        if log["cost"] > budget_threshold:
            print(f" Agent {log['agent']} exceeds budget: ${log['cost']}")
            return False
    return True
