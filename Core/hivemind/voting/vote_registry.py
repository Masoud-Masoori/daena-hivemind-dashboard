def register_votes(vote_data):
    tally = {}
    for vote in vote_data:
        key = vote["topic"]
        tally[key] = tally.get(key, 0) + 1
    return tally
