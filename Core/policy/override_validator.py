def validate_override(agent, reason):
    return f"[Override]  Agent: {agent} requested override for: {reason}"

if __name__ == "__main__":
    print(validate_override("LLM-Fusion", "Context conflict"))
