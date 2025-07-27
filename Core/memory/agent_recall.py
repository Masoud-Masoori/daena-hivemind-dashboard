def recall_agent_context(agent_name):
    memory = {
        "Daena": "Central orchestrator with override authority",
        "FinanceBot": "Tracks budget and reports expenditures",
        "Lingovids": "Multilingual transcription assistant"
    }
    return f"[Recall]  {agent_name}: {memory.get(agent_name, 'No memory found')}"

if __name__ == "__main__":
    print(recall_agent_context("Daena"))
