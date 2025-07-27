def route_task(task):
    if "creative" in task:
        return "openai"
    elif "translation" in task:
        return "gemini"
    elif "speed" in task:
        return "groq"
    return "reflex"
