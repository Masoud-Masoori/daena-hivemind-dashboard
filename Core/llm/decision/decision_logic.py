def select_best_response(scored_responses):
    return max(scored_responses, key=lambda x: x["score"])
