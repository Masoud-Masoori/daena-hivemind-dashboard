from Core.agents.agent import Agent as BaseAgent

class SalesAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[SalesAgent] Received message: {content}")
        # Example: if it's a customer inquiry, prepare a response
        if "customer" in content.lower() or "inquiry" in content.lower():
            response = f"Thank you for reaching out. Regarding \"{content}\", here is the information..."
            print(f"[SalesAgent] Responding: {response}")
            self.memory.store({"last_response": response})
            # In real use, might send email or chat via integration
