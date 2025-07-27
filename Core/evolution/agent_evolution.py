### File: core/evolution/agent_evolution.py

import json
import os

EVOLUTION_LOG = "D:/Ideas/Daena/logs/evolution.json"

def log_agent_behavior(agent_name, feedback, rating):
    log = {}
    if os.path.exists(EVOLUTION_LOG):
        with open(EVOLUTION_LOG, "r") as f:
            log = json.load(f)
    if agent_name not in log:
        log[agent_name] = []
    log[agent_name].append({"feedback": feedback, "rating": rating})
    with open(EVOLUTION_LOG, "w") as f:
        json.dump(log, f, indent=2)

def summarize_agent_learning(agent_name):
    if not os.path.exists(EVOLUTION_LOG): return {}
    with open(EVOLUTION_LOG, "r") as f:
        log = json.load(f)
    return log.get(agent_name, [])
