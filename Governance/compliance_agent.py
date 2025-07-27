from Core.agents.agent import Agent as BaseAgent

class ComplianceAgent(BaseAgent):
    def __init__(self, name, bus, memory, config=None, watched_agents=None):
        super().__init__(name, bus, memory, config)
        self.watched_agents = watched_agents or {}

    def handle_message(self, message):
        content = message.get("content", "") or ""
        sender = message.get("from", "")
        # Simple check: block content containing forbidden terms
        forbidden_terms = ["illegal", "confidential"]
        for term in forbidden_terms:
            if term in content.lower():
                print(f"[ComplianceAgent] Blocked message from {sender} containing '{term}'.")
                return False
        # Otherwise, allow and log
        self.memory.store({"compliance_checked": f"{sender}: {content}"})
        return True
