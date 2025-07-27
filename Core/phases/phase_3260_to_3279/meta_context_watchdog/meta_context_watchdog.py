# meta_context_watchdog.py

import time

last_focus = {}

def update_focus(agent_id, task):
    last_focus[agent_id] = (task, time.time())
    print(f"[WATCHDOG] {agent_id} is working on {task}")

def get_focus(agent_id):
    task, timestamp = last_focus.get(agent_id, ("Nothing", 0))
    return task

def print_focus():
    for agent, (task, t) in last_focus.items():
        print(f"{agent}  {task}")
