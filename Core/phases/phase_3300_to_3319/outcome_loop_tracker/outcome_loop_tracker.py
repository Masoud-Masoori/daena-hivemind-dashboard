# outcome_loop_tracker.py

outcome_history = {}

def track(agent_id, result):
    if agent_id not in outcome_history:
        outcome_history[agent_id] = []
    outcome_history[agent_id].append(result)

def last_result(agent_id):
    return outcome_history.get(agent_id, [])[-1] if agent_id in outcome_history and outcome_history[agent_id] else None

def loop_detected(agent_id):
    results = outcome_history.get(agent_id, [])
    return len(results) >= 3 and results[-1] == results[-2] == results[-3]
