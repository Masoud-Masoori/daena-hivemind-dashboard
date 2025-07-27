def override_swarm(agent_status):
    over = [a for a in agent_status if a["mode"] == "rogue"]
    if over:
        return f"[SwarmOverride]  Overriding: {[a['id'] for a in over]}"
    return "[SwarmOverride]  All agents stable."

if __name__ == "__main__":
    test = [{"id": "a1", "mode": "active"}, {"id": "x2", "mode": "rogue"}]
    print(override_swarm(test))
