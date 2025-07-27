# autonomy_reflector.py

def reflect_autonomy(agent_id, last_decision, outcome):
    print(f"[AutonomyReflector]  Agent {agent_id} reflecting on autonomy...")
    if "error" in outcome.lower():
        print(f"[AutonomyReflector]  Detected failure. Decision was: {last_decision}")
        return "override"
    return "proceed"
