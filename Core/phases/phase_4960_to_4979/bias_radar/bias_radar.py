# bias_radar.py
class BiasRadar:
    def __init__(self):
        self.bias_records = {}

    def detect_bias(self, agent_name, topic, polarity):
        if agent_name not in self.bias_records:
            self.bias_records[agent_name] = {}
        self.bias_records[agent_name][topic] = polarity

    def get_bias_report(self, agent_name):
        return self.bias_records.get(agent_name, {})
