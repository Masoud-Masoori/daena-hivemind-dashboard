# Mobile fallback handler
def mobile_sync(agent_state):
    if agent_state["device"] == "mobile":
        return "Use lightweight LLM API"
