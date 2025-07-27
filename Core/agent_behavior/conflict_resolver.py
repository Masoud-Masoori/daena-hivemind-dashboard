def resolve_conflict(agent1_decision, agent2_decision):
    if agent1_decision == agent2_decision:
        return agent1_decision
    else:
        return "[CONFLICT] Human Override Needed"

if __name__ == "__main__":
    print("[Conflict] ", resolve_conflict("Enable Feature X", "Disable Feature X"))
