# synaptic_trace.py
class SynapticLink:
    def __init__(self):
        self.trace_map = []

    def log_decision(self, origin, trigger, decision):
        self.trace_map.append({
            "origin": origin,
            "trigger": trigger,
            "decision": decision
        })

    def backtrack(self, steps=5):
        return self.trace_map[-steps:]
