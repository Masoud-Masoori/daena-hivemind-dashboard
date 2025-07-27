def check_llm_compat(model, task_size):
    limits = {
        "openai": 16000,
        "gemini": 32000,
        "groq": 8000,
        "reflex": 4000
    }
    return task_size <= limits.get(model, 2048)
