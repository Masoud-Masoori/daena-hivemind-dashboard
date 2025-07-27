def resolve_conflict(agentA, agentB, task):
    # Example: resolve by trust score or availability
    decision = agentA if agentA < agentB else agentB
    print(f"[RESOLVE] {task}  assigned to {decision}")
    return decision
