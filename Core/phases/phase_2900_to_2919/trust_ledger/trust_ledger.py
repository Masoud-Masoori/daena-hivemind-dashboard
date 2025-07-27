# trust_ledger.py

agent_scores = {}

def update_trust(agent_id, outcome, weight=1.0):
    if agent_id not in agent_scores:
        agent_scores[agent_id] = 0.5
    adjustment = 0.05 * weight if outcome else -0.05 * weight
    agent_scores[agent_id] = max(0.0, min(1.0, agent_scores[agent_id] + adjustment))
    print(f"[TrustLedger]  Agent {agent_id} trust score updated to {agent_scores[agent_id]:.2f}")
    return agent_scores
