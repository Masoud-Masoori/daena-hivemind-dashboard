def predict_failure(agent_state):
    if "overload" in agent_state.lower():
        print("Potential fault detected: Agent overloaded.")
        return True
    return False
