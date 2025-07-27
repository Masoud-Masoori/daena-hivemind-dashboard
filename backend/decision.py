import json, os

def get_agent_policy(agent):
    path = f"agent_models/{agent}/config.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"preferredLLM": "DeepSeek"}

def decide_response(agent, llm_responses):
    policy = get_agent_policy(agent)
    preferred = policy.get("preferredLLM", "DeepSeek")
    response = llm_responses.get(preferred)
    if not response:
        response = list(llm_responses.values())[0]
    return {
        "chosen": preferred,
        "response": response,
        "all": llm_responses
    }
