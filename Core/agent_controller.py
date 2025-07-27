from core.llm_router import route_to_model

def handle_prompt(prompt):
    print(f"[Agent Controller] Input received: {prompt}")
    model_decision = route_to_model(prompt)
    return f"{model_decision} [Simulated Agent Handling]"
