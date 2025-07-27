def vote_on_responses(responses):
    votes = {}
    for r in responses:
        content = r["response"]
        votes[content] = votes.get(content, 0) + 1
    return max(votes.items(), key=lambda x: x[1])[0]
