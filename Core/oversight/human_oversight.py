def escalate_to_human(event):
    return f"[Oversight]  Human attention required for: {event}"

if __name__ == "__main__":
    print(escalate_to_human("Policy breach detected in Agent-Finance"))
