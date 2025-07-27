def agent_vote(decisions):
    votes = {d: decisions.count(d) for d in set(decisions)}
    result = max(votes, key=votes.get)
    return f"[Voting]  Winner: {result} with {votes[result]} votes"

if __name__ == "__main__":
    print(agent_vote(["Plan A", "Plan B", "Plan A", "Plan C", "Plan A"]))
