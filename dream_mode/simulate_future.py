import random, json, time

SCENARIOS = [
    {"situation": "market_crash", "response": "shift_investments", "impact": -0.3},
    {"situation": "AI_regulation", "response": "compliance_layer", "impact": +0.1},
    {"situation": "data_breach", "response": "quarantine_module", "impact": -0.2},
    {"situation": "agent_failure", "response": "retrain_subagent", "impact": +0.05}
]

def simulate():
    print("\n [Daena Dream Mode] Starting hypothetical simulation...")
    results = []
    for _ in range(5):
        s = random.choice(SCENARIOS)
        print(f"\n Simulating: {s['situation']}")
        time.sleep(1)
        result = {
            "situation": s["situation"],
            "suggested_response": s["response"],
            "impact": s["impact"]
        }
        results.append(result)

    with open('D:/Ideas/Daena/dream_mode/simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n Simulation complete. Results saved to simulation_results.json")

# simulate()
