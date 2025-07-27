from core.optimizer.brain_optimizer import optimize_llm_response
from core.blockchain.hive_ledger import BlockchainLogger
from core.diagnostics.agent_diagnostics import agent_diagnostics_report

def run_launch_protocol():
    print(" Optimizing LLM selection...")
    dummy_responses = [
        {"model": "qwen", "score": 0.75},
        {"model": "deepseek-r2", "score": 0.88},
        {"model": "yi-6b", "score": 0.83}
    ]
    best = optimize_llm_response(dummy_responses)
    print(f" Best LLM selected: {best['model']}")

    print(" Generating diagnostics...")
    agent_diagnostics_report()

    print(" Writing blockchain log...")
    BlockchainLogger().log({
        "event": "launch",
        "selected_llm": best["model"]
    })

    print(" Daena launch protocol completed.")

if __name__ == "__main__":
    run_launch_protocol()
