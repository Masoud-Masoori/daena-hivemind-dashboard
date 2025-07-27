# root_truth_ledger.py
import hashlib
import json

class RootTruthLedger:
    def __init__(self):
        self.chain = []

    def add_entry(self, data):
        entry = {
            "index": len(self.chain),
            "data": data,
            "hash": self._hash_data(data)
        }
        self.chain.append(entry)

    def _hash_data(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def verify(self, index, data):
        expected_hash = self._hash_data(data)
        return self.chain[index]["hash"] == expected_hash if index < len(self.chain) else False
