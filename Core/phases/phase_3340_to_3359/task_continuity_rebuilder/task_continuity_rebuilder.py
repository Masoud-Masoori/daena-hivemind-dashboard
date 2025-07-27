# task_continuity_rebuilder.py

task_checkpoint = {}

def checkpoint(agent_id, task_info):
    task_checkpoint[agent_id] = task_info

def resume(agent_id):
    return task_checkpoint.get(agent_id, None)
