# consistency_evaluator.py

def evaluate(agent_id, decisions):
    stable = all(d == decisions[0] for d in decisions)
    if not stable:
        print(f"[INCONSISTENCY] {agent_id} shows variation: {decisions}")
    return stable
