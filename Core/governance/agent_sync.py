def sync_agents(agent_statuses):
    synced = all(status == "OK" for status in agent_statuses.values())
    return f"[AgentSync] {' All agents synchronized' if synced else ' Desync detected!'}"

if __name__ == "__main__":
    print(sync_agents({"vision": "OK", "voice": "OK", "planner": "DESYNC"}))
