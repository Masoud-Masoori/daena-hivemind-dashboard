### File: core/ledger/agent_blocklog.py

import json, hashlib, time

LEDGER_PATH = "D:/Ideas/Daena/core/ledger/chain.json"

def hash_block(block): return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def create_block(agent, action, result):
    block = {
        "timestamp": time.time(),
        "agent": agent,
        "action": action,
        "result": result
    }
    block["hash"] = hash_block(block)
    return block

def append_block(block):
    try:
        with open(LEDGER_PATH, "r") as f: chain = json.load(f)
    except: chain = []
    chain.append(block)
    with open(LEDGER_PATH, "w") as f: json.dump(chain, f, indent=2)
