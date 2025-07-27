# agent_trace_auditor.py
class AgentTraceAuditor:
    def __init__(self):
        self.traces = []

    def log_action(self, agent_id, action, outcome):
        self.traces.append({
            "agent_id": agent_id,
            "action": action,
            "outcome": outcome
        })

    def trace_for_agent(self, agent_id):
        return [t for t in self.traces if t["agent_id"] == agent_id]
