# sync_bridge.py
import json
from pathlib import Path

SYNC_FILE = Path("D:/Ideas/Daena/status/active_projects.json")

def get_synced_projects():
    if SYNC_FILE.exists():
        return json.loads(SYNC_FILE.read_text())
    return {}

def update_sync(project, phase):
    data = get_synced_projects()
    data[project] = phase
    SYNC_FILE.write_text(json.dumps(data, indent=2))
    print(f"[SyncBridge] Synced {project} @ Phase {phase}")
