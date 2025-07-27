# decision_echo_guard.py
recent_decisions = {}

def is_duplicate_decision(agent_id, decision_hash):
    if agent_id in recent_decisions and recent_decisions[agent_id] == decision_hash:
        return True
    recent_decisions[agent_id] = decision_hash
    return False
