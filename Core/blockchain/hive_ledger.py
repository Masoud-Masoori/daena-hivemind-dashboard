import json
from datetime import datetime
import hashlib

class BlockchainLogger:
    def __init__(self, log_file="core/blockchain/hive_ledger.json"):
        self.log_file = log_file

    def _hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def log(self, entry):
        try:
            with open(self.log_file, "r") as f:
                chain = json.load(f)
        except:
            chain = []

        entry["timestamp"] = datetime.utcnow().isoformat()
        entry["hash"] = self._hash(entry)
        chain.append(entry)

        with open(self.log_file, "w") as f:
            json.dump(chain, f, indent=2)
