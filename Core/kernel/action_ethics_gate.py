import json

def load_constitution():
    with open("D:/Ideas/Daena/core/kernel/ai_constitution.json") as f:
        return json.load(f)["rules"]

def ethics_score(action_desc):
    rules = load_constitution()
    score = sum([1 for r in rules if r.lower() in action_desc.lower()])
    print(f"[ETHICS] Action score: {score}/{len(rules)}")
    return score >= 2
