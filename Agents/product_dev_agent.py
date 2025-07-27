from Core.agents.agent import Agent as BaseAgent

class ProductDevAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[ProductDevAgent] Received message: {content}")
        # Example: if told to develop a feature
        if "feature" in content.lower() or "develop" in content.lower():
            self.think(f"Designing and coding for request: {content}")
            # ... code generation would happen here
            self.memory.store({"dev_task_completed": content})
            # Notify others, e.g., Marketing that feature is ready (if appropriate)
            # self.send_message("Marketing", f"Feature done: {content}")
