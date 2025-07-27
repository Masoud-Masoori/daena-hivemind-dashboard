# governed_override.py

import json

OVERRIDE_POLICY_PATH = 'D:/Ideas/Daena/core/ethics/override_policies.json'

def load_override_policies():
    try:
        with open(OVERRIDE_POLICY_PATH, 'r') as file:
            return json.load(file)
    except:
        return {}

def is_override_allowed(agent_id, action):
    policies = load_override_policies()
    return policies.get(agent_id, {}).get('allow', []).count(action) > 0
