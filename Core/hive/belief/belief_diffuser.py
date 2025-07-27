def diffuse_belief(source_belief, agents):
    for agent in agents:
        print(f"[BeliefDiffuser] Synced belief to {agent}: {source_belief}")

if __name__ == "__main__":
    diffuse_belief("Trust protocol-47", ["AgentX", "AgentY", "AgentZ"])
