### File: core/hiveops/hive_ops_daemon.py

import os, time, json
from datetime import datetime

AGENT_DIR = "D:/Ideas/Daena/agents"
HEARTBEAT_LOG = "D:/Ideas/Daena/core/hiveops/heartbeat.json"

def scan_agents():
    statuses = {}
    for agent in os.listdir(AGENT_DIR):
        path = os.path.join(AGENT_DIR, agent)
        alive = os.path.isdir(path) and os.path.exists(os.path.join(path, "agent_meta.json"))
        statuses[agent] = {
            "status": "online" if alive else "missing",
            "last_checked": datetime.now().isoformat()
        }
    with open(HEARTBEAT_LOG, "w") as f: json.dump(statuses, f, indent=2)

def run_heartbeat_loop():
    print("[HiveOps]  Heartbeat scanning started...")
    while True:
        scan_agents()
        time.sleep(15)
