import json

class BrainOptimizer:
    def __init__(self, log_path="core/diagnostics/agent_report.json"):
        self.log_path = log_path

    def evaluate_responses(self, responses):
        scored = sorted(responses, key=lambda x: x.get("score", 0), reverse=True)
        return scored[0] if scored else {}

    def record_result(self, result):
        with open(self.log_path, "w") as f:
            json.dump(result, f, indent=2)

def optimize_llm_response(responses):
    brain = BrainOptimizer()
    best = brain.evaluate_responses(responses)
    brain.record_result(best)
    return best
