def fallback_handler(error_type):
    mapping = {
        "timeout": "Try reducing prompt length.",
        "no_response": "Ask again or use cached memory.",
        "crash": "Switch to alternate LLM."
    }
    return mapping.get(error_type, "Generic fallback applied.")

if __name__ == "__main__":
    print("[Fallback]", fallback_handler("timeout"))
