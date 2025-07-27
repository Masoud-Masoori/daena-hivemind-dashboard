def debate(models):
    votes = {m: len(r) for m, r in models.items()}
    return max(votes, key=votes.get)

if __name__ == "__main__":
    result = debate({"Qwen": ["Yes", "Yes"], "R2": ["No"], "Yi": ["Yes"]})
    print("[Debate Winner] :", result)
