def fetch_trust_score(agent_id, ledger):
    return ledger.get(agent_id, {}).get("trust_score", 0.5)
