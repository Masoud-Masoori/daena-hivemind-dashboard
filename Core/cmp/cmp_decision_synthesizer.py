def synthesize(agent_votes):
    score_map = {}
    for vote in agent_votes:
        task = vote["task"]
        score_map[task] = score_map.get(task, 0) + vote["confidence"]
    best = max(score_map.items(), key=lambda x: x[1])
    print(f"[SYNTHESIZER] Best Action: {best[0]} (score={best[1]})")
    return best[0]
