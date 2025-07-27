def score_conversation(response, context):
    score = 0
    if context in response:
        score += 5
    if "insight" in response.lower():
        score += 3
    return score
