def train_response(agent_input):
    if "confused" in agent_input.lower():
        return "Recalibrating response pattern..."
    return "Response pattern stable."
