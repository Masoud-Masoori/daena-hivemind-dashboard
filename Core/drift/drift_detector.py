### File: core/drift/drift_detector.py

import json, os

AGENT_META_DIR = "D:/Ideas/Daena/agents"
DRIFT_LOG = "D:/Ideas/Daena/logs/drift_report.json"

def detect_drift():
    drift = {}
    for agent in os.listdir(AGENT_META_DIR):
        meta_path = os.path.join(AGENT_META_DIR, agent, "agent_meta.json")
        if not os.path.exists(meta_path): continue
        with open(meta_path) as f:
            data = json.load(f)
        expected = data.get("expected_focus")
        current = data.get("current_focus")
        if expected and current and expected != current:
            drift[agent] = {
                "expected": expected,
                "current": current
            }
    with open(DRIFT_LOG, "w") as f:
        json.dump(drift, f, indent=2)
    print(f"[DriftControl]  Detected drifts: {list(drift.keys())}")
