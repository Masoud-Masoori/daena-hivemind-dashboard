# priority_weigher.py

def reweigh_priorities(task_queue):
    print("[PriorityWeigher]  Rebalancing task queue based on urgency and dependencies...")
    sorted_tasks = sorted(task_queue, key=lambda t: (t['urgency'], -t['age']), reverse=True)
    return sorted_tasks
