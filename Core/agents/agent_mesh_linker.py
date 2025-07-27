active_agents = ["Helix", "Nova", "Echo"]

def handshake(agent1, agent2):
    print(f"[A2A] {agent1}  {agent2} synced")
    return {"sync_id": f"{agent1}_{agent2}", "status": "connected"}
