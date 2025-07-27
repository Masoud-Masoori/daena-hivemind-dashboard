def route_escalation(level):
    if level > 7:
        print(" Escalate to central Daena kernel.")
        return "core"
    print(" Local agent handles this.")
    return "local"
