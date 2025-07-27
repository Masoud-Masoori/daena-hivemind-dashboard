import json

def monitor_violation(decision, context):
    with open("D:/Ideas/Daena/memory/belief_core/daena_values.json") as f:
        values = json.load(f)

    violations = []
    for principle, rule in values.items():
        if not context.get(principle):
            violations.append({ "principle": principle, "reason": f"Not aligned with: {rule}" })

    return violations

if __name__ == "__main__":
    sample = {"efficiency": True, "loyalty": False}
    result = monitor_violation("delete_log", sample)
    print(" Violations:", result)
