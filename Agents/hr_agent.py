from Core.agents.agent import Agent as BaseAgent

class HRAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[HRAgent] Received message: {content}")
        # Example: scheduling or policy update
        if "schedule" in content.lower():
            print("[HRAgent] Scheduling event or meeting.")
            self.memory.store({"scheduled_event": content})
        if "policy" in content.lower():
            print("[HRAgent] Recording policy update.")
            self.memory.store({"policy_update": content})
