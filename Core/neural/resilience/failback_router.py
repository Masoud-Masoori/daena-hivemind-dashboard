def failback_route(agent_name):
    return {"agent": agent_name, "fallback": "backup_node_AI", "status": "standby_ready"}

if __name__ == "__main__":
    print("[Failback] ", failback_route("Nova"))
