def resolve_conflict(agent_opinions):
    tally = {}
    for opinion in agent_opinions:
        tally[opinion] = tally.get(opinion, 0) + 1
    resolution = max(tally, key=tally.get)
    return f"[Resolver] Consensus: {resolution}"

if __name__ == "__main__":
    print(resolve_conflict(["use_R2", "use_R2", "use_Qwen"]))
