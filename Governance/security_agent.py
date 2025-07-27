from Core.agents.agent import Agent as BaseAgent

class SecurityAgent(BaseAgent):
    def __init__(self, name, bus, memory, config=None, watched_agents=None):
        super().__init__(name, bus, memory, config)
        self.watched_agents = watched_agents or {}

    def handle_message(self, message):
        content = message.get("content", "") or ""
        sender = message.get("from", "")
        # Simple monitor: log external link access attempts
        if "http://" in content or "https://" in content:
            print(f"[SecurityAgent] {sender} attempted to access URL: {content}")
            self.memory.store({"url_access": f"{sender}: {content}"})
        # Additional security checks would be added here
