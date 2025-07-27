def evolve(agent_state):
    upgrades = {"stale": "v2", "v2": "v3", "v3": "v4"}
    return f"[Evolve]  Agent upgraded to {upgrades.get(agent_state, 'v1')}"

if __name__ == "__main__":
    print(evolve("stale"))
