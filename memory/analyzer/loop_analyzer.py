import os, json, time
from collections import defaultdict

LOG_DIR = 'D:/Ideas/Daena/memory/logs'
THRESHOLD_REPETITION = 3

def analyze_loops():
    patterns = defaultdict(list)
    for file in os.listdir(LOG_DIR):
        if not file.endswith('.json'): continue
        with open(os.path.join(LOG_DIR, file)) as f:
            data = json.load(f)
            key = data.get("task_signature")
            patterns[key].append(data)

    for key, items in patterns.items():
        if len(items) >= THRESHOLD_REPETITION:
            print(f"[] Pattern '{key}' repeated {len(items)} times. Triggering loop breaker.")
            suggest_intervention(key, items)

def suggest_intervention(pattern, entries):
    print(f"\n Suggested Fix for Loop '{pattern}':")
    print(f"- Vary task input or agent context.")
    print(f"- Assign to a different department or escalate.")
    print(f"- Consider terminating task loop if no progress.")

# analyze_loops()
