def escalate_issue(agent_id, issue_level):
    if issue_level > 7:
        print(f"[ESCALATION] Critical alert for agent {agent_id}")
    else:
        print(f"[ESCALATION] Agent {agent_id} flagged at level {issue_level}")
