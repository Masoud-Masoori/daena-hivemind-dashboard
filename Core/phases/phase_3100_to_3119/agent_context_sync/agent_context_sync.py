# agent_context_sync.py

import json
import os

def sync_agent_context(agent_id, context):
    path = os.path.join("D:/Ideas/Daena/agents/context", f"{agent_id}_context.json")
    with open(path, 'w') as f:
        json.dump(context, f, indent=4)
    print(f"[Sync]  Agent '{agent_id}' context synchronized.")
