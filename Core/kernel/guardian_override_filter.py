import json

def load_constitution():
    with open("D:/Ideas/Daena/core/kernel/ai_constitution.json") as f:
        return json.load(f)["rules"]

def ethics_score(action_desc):
    rules = load_constitution()
    score = sum([1 for r in rules if r.lower(]()
$cmpPath = "D:\Ideas\Daena\core\cmp"
$kernelPath = "D:\Ideas\Daena\core\kernel"
$dashFeedPath = "D:\Ideas\Daena\ui\dashboard\feed"

# 1. Guardian Override Filter
@'
def override_guard(action):
    if "self-harm" in action["tags"] or action["cost"] > 5000:
        print("[GUARDIAN] Blocked critical action for review.")
        return False
    return True
