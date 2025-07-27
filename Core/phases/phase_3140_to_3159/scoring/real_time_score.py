# real_time_score.py

import random

AGENT_SCORES = {}

def update_score(agent_id, task_result):
    score = round(random.uniform(0.0, 1.0), 2) if task_result['status'] == 'completed' else 0.0
    AGENT_SCORES[agent_id] = score
    print(f"[Score] {agent_id} scored {score}")
    return score
