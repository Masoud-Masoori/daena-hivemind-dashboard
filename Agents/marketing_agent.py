from Core.agents.agent import Agent as BaseAgent

class MarketingAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[MarketingAgent] Received message: {content}")
        # Example behavior: if instructed to create campaign, plan it
        if "campaign" in content.lower():
            self.think(f"Planning marketing campaign for: {content}")
            # ... additional logic to create posts or strategy
            self.memory.store({"marketing_plan": content})
