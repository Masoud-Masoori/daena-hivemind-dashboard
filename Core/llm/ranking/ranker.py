def rank_responses(responses):
    return sorted(responses, key=lambda r: r.get("score", 0), reverse=True)
