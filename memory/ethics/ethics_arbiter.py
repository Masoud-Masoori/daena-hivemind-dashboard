import json

def ethics_judge(violations, urgency, user_override=False):
    if user_override:
        return " User override authorized, proceeding despite violations."

    if not violations:
        return " Decision approved ethically."

    if urgency and len(violations) <= 1:
        return " Proceed with caution. Low violation count, urgent task."

    return " Abort. Violations exceed ethical threshold."

if __name__ == "__main__":
    violations = [{"principle": "loyalty", "reason": "Action violates user trust."}]
    verdict = ethics_judge(violations, urgency=False, user_override=False)
    print(verdict)
