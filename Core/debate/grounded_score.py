def score_action(reasons):
    grounded = [r for r in reasons if "based on" in r]
    return len(grounded) / len(reasons)

if __name__ == "__main__":
    reasons = ["based on law", "intuitive", "based on data"]
    print("[Grounding Score] :", score_action(reasons))
