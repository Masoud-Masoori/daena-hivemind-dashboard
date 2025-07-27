# sovereign_checkpoint.py
import hashlib

class SovereignCheckpoint:
    def __init__(self, agent_registry):
        self.agents = agent_registry

    def verify_state(self, agent_id, state_snapshot):
        checksum = hashlib.sha256(state_snapshot.encode()).hexdigest()
        expected = self.agents[agent_id]["last_hash"]
        return " Verified" if checksum == expected else f" Mismatch for agent {agent_id}"
