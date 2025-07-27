def escalate(issue, level):
    return f"[Escalation]  Issue: {issue} | Escalated to level {level}"

if __name__ == "__main__":
    print(escalate("Model drift detected", 2))
