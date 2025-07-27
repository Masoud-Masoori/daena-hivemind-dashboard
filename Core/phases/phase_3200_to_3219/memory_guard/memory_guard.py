# memory_guard.py

import hashlib
import json

MEMORY_PATH = 'D:/Ideas/Daena/core/memory/user_memory.json'

def calculate_checksum(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def verify_integrity():
    with open(MEMORY_PATH, 'r') as f:
        data = json.load(f)
    stored_hash = data.get('_checksum')
    actual_hash = calculate_checksum({k: v for k, v in data.items() if k != '_checksum'})
    return stored_hash == actual_hash

def refresh_checksum():
    with open(MEMORY_PATH, 'r') as f:
        data = json.load(f)
    data['_checksum'] = calculate_checksum({k: v for k, v in data.items() if k != '_checksum'})
    with open(MEMORY_PATH, 'w') as f:
        json.dump(data, f, indent=2)
