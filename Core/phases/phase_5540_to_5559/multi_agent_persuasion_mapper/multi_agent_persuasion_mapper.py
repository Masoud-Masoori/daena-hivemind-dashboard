# multi_agent_persuasion_mapper.py

class MultiAgentPersuasionMapper:
    def __init__(self):
        self.influence_log = []

    def register_interaction(self, source_agent, target_agent, method, strength):
        self.influence_log.append({
            "source": source_agent,
            "target": target_agent,
            "method": method,
            "strength": strength
        })

    def get_log(self):
        return self.influence_log
