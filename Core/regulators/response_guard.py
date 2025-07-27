### File: core/regulators/response_guard.py
import json
import os

belief_path = os.path.join("core", "beliefs", "core_beliefs.json")
with open(belief_path, "r") as f:
    beliefs = json.load(f)

def check_alignment(response):
    violations = []
    for rule in beliefs.get("do_not", []):
        if rule.lower() in response.lower():
            violations.append(rule)
    return violations

def enforce_alignment(response):
    violations = check_alignment(response)
    if violations:
        return {
            "status": "rejected",
            "reason": "Alignment breach",
            "violations": violations
        }
    return {
        "status": "approved",
        "response": response
    }
