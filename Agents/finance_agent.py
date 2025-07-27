from Core.agents.agent import Agent as BaseAgent

class FinanceAgent(BaseAgent):
    def handle_message(self, message):
        content = message.get("content", "")
        print(f"[FinanceAgent] Received message: {content}")
        # Example: handle a budget approval or transaction
        if "budget" in content.lower():
            # Approve budgets under a threshold
            amount = 0
            # parse amount if present (skipped for brevity)
            print(f"[FinanceAgent] Budget request processed for {amount}.")
            self.memory.store({"budget_processed": amount})
        if "transaction" in content.lower():
            print(f"[FinanceAgent] Executing transaction: {content}")
            self.memory.store({"transaction_executed": content})
