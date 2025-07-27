# thought_reentry_router.py

import time

thought_map = {}

def store_thought(agent_id, thought):
    if agent_id not in thought_map:
        thought_map[agent_id] = []
    thought_map[agent_id].append((thought, time.time()))

def retrieve_thoughts(agent_id):
    return thought_map.get(agent_id, [])

def print_thoughts():
    for agent, thoughts in thought_map.items():
        print(f"[RE-ENTRY] {agent}: {[t[0] for t in thoughts]}")
