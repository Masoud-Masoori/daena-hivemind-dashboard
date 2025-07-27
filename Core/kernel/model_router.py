import os
import random
from cmp.guardian import confirm_action

def choose_model(input_text):
    local_models = ["deepseek_r2", "qwen", "gemma"]
    api_keys = {
        "openai": os.getenv("OPENAI_API_KEY"),
        "gemini": os.getenv("GEMINI_API_KEY"),
        "grok": os.getenv("GROk_API_KEY"),
        "claude": os.getenv("ANTHROPIC_API_KEY"),
        "deepseek": os.getenv("DDEESEEK_API_KEY")
    }

    # Try local first
    for model in local_models:
        try:
            print(f" [ModelRouter] Trying local model: {model}")
            # Simulated logic
            if random.random() > 0.3:
                return f"[LOCAL SUCCESS] Response from {model}"
        except:
            continue

    # Else fallback to API (CMP confirmation first)
    for api, key in api_keys.items():
        if key:
            proceed = confirm_action(f"Use {api} API? May incur cost.")
            if proceed:
                print(f" [ModelRouter] Fallback to {api} API")
                return f"[API SUCCESS] Response from {api}"
    return "[FAIL] No response available"
