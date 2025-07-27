# intention_trace.py
import json
import os

TRACE_FILE = "D:/Ideas/Daena/logs/intention_trail.json"

def log_intention(step, context):
    os.makedirs(os.path.dirname(TRACE_FILE), exist_ok=True)
    trail = []
    if os.path.exists(TRACE_FILE):
        with open(TRACE_FILE, 'r') as f:
            try:
                trail = json.load(f)
            except json.JSONDecodeError:
                pass
    trail.append({"step": step, "context": context})
    with open(TRACE_FILE, 'w') as f:
        json.dump(trail, f, indent=2)
