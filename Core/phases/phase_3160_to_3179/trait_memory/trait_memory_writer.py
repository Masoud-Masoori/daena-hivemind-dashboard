# trait_memory_writer.py

import json
from datetime import datetime

TRAIT_LOG = "D:/Ideas/Daena/core/ethics/trait_history.json"

def write_trait_snapshot(agent_id, traits):
    snapshot = {
        'agent': agent_id,
        'traits': traits,
        'timestamp': datetime.utcnow().isoformat()
    }
    try:
        with open(TRAIT_LOG, 'a') as file:
            file.write(json.dumps(snapshot) + '\n')
        print(f"[TraitMemory] Logged traits for {agent_id}")
    except Exception as e:
        print(f"[Error] Trait logging failed: {e}")
