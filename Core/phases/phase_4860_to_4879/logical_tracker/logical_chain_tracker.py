# logical_chain_tracker.py
class LogicalChainTracker:
    def __init__(self):
        self.logic_chains = {}

    def track(self, agent_id, reasoning_steps):
        self.logic_chains[agent_id] = reasoning_steps
        return True

    def get_trace(self, agent_id):
        return self.logic_chains.get(agent_id, [])
