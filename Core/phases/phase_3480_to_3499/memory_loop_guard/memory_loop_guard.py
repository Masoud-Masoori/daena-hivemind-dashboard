# memory_loop_guard.py

from collections import defaultdict

loop_tracker = defaultdict(int)

def track_step(agent_id, step_key):
    loop_tracker[(agent_id, step_key)] += 1
    return loop_tracker[(agent_id, step_key)] > 5

def flag_loop(agent_id, step_key):
    if track_step(agent_id, step_key):
        return f" Loop detected in agent {agent_id} at '{step_key}'"
    return " No loop detected"
