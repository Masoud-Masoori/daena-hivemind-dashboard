# memory_anchor.py

import datetime

def drop_memory_anchor(event_id, agent_name):
    anchor = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'agent': agent_name,
        'event': event_id
    }
    print(f"[MemoryAnchor]  Anchor dropped: {anchor}")
    return anchor
