# meta_agent_verifier.py
class MetaAgentVerifier:
    def __init__(self, agent_registry):
        self.registry = agent_registry

    def verify_meta_structure(self):
        return all("role" in agent and "auth_level" in agent for agent in self.registry)
