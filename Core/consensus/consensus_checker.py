### File: core/consensus/consensus_checker.py

def vote_from_llms(query, responses):
    counts = {}
    for r in responses:
        key = r.get("model", "unknown")
        counts[key] = counts.get(key, 0) + 1

    winner = max(counts.items(), key=lambda x: x[1])
    return winner[0], counts
