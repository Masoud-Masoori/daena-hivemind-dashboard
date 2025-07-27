import json, hashlib, time
from pathlib import Path

BLOCKCHAIN_DIR = Path('D:/Ideas/Daena/blockchain/ledger')
KEY = 'super_secret_key_for_daena_2025'

def hash_block(block):
    block_str = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_str).hexdigest()

def create_block(action, previous_hash):
    block = {
        "index": len(list(BLOCKCHAIN_DIR.glob('*.json'))),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": action,
        "previous_hash": previous_hash,
        "signature": f"signed:{KEY}",
    }
    block["hash"] = hash_block(block)
    with open(BLOCKCHAIN_DIR / f"{block['index']:04d}_block.json", "w") as f:
        json.dump(block, f, indent=2)

# Example:
# create_block("LLM decision made by DeepSeek-R2", "ROOT_HASH")
