# offline_resolver.py
import os
import json

QUEUE_FILE = "D:/Ideas/Daena/logs/offline_queue.json"

def add_task(task):
    queue = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except json.JSONDecodeError:
                pass
    queue.append(task)
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

def resolve_pending_tasks():
    if not os.path.exists(QUEUE_FILE):
        print("[Resolver] No offline tasks found.")
        return
    with open(QUEUE_FILE, 'r') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            print("[Resolver] Queue corrupt.")
            return
    for task in tasks:
        print(f"[Resolver] Handling task: {task}")
    os.remove(QUEUE_FILE)
