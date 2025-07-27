def distribute_load(agent_loads):
    total = sum(agent_loads.values())
    return {k: round((v / total), 2) for k, v in agent_loads.items()}

if __name__ == "__main__":
    loads = {"Nova": 30, "Helix": 40, "Echo": 30}
    print("[LoadBalance] ", distribute_load(loads))
