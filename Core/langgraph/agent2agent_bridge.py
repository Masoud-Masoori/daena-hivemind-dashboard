def initiate_agent_sync(agent_list):
    print("[LangGraph] Syncing agents:", ", ".join(agent_list))
    return {"status": "synced", "agents": agent_list}
