import random

def choose_llm(prompt):
    if \"code\" in prompt.lower():
        return \"deepseek-r2\"
    elif \"translate\" in prompt.lower() or \"language\" in prompt.lower():
        return \"qwen2.5\"
    elif \"summarize\" in prompt.lower():
        return \"yi-6b\"
    else:
        return random.choice([\"deepseek-r2\", \"qwen2.5\", \"yi-6b\"])

def route_to_model(prompt):
    model = choose_llm(prompt)
    print(f\"[LLM Router] Routing to: {model}\")
    return f\"{model} will handle this task.\"
