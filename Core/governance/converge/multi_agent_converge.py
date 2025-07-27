def converge_agents(agent_outputs):
    return max(set(agent_outputs), key=agent_outputs.count)

if __name__ == "__main__":
    print("[Multi-Agent Converge] Final decision:", converge_agents(["yes", "no", "yes", "yes"]))
