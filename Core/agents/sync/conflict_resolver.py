def resolve_conflicts(agent_outputs):
    votes = {}
    for out in agent_outputs:
        votes[out] = votes.get(out, 0) + 1
    return max(votes, key=votes.get)
