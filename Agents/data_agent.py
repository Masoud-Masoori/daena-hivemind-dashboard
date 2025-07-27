from Core.agents.agent import Agent as BaseAgent

class DataAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[DataAgent] Received message: {content}")
        # Example: perform a research task
        if "research" in content.lower() or "find" in content.lower():
            info = "Sample market insight: ... (dummy data)."
            print(f"[DataAgent] Providing research result.")
            self.memory.store({"research_result": info})
            # Optionally, reply to requester
            if message.get("from"):
                self.send_message(message["from"], f"ResearchResult: {info}")
