# Ranks thread response by urgency and accuracy
def rank_responses(responses):
    return sorted(responses, key=lambda r: r["confidence"] * r["urgency"], reverse=True)
