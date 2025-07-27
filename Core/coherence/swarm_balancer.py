def balance_swarm(agents):
    max_load = max(agents.values())
    balanced = {k: v - (max_load - v) for k, v in agents.items()}
    return f"[Balancer]  Load distributed: {balanced}"

if __name__ == "__main__":
    print(balance_swarm({"alpha": 8, "beta": 5, "gamma": 3}))
