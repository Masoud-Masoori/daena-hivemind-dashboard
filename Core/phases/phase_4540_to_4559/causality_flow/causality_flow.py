# causality_flow.py
import uuid
import datetime

class CausalityFlow:
    def __init__(self):
        self.map = []

    def trace_action(self, agent_id, input_data, output_data):
        self.map.append({
            "uuid": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "agent_id": agent_id,
            "input": input_data,
            "output": output_data
        })

    def get_trace(self):
        return self.map
