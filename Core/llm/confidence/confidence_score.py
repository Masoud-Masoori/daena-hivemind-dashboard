def estimate_confidence(response):
    # Dummy heuristic
    if "definitely" in response.lower():
        return 0.9
    elif "maybe" in response.lower():
        return 0.5
    return 0.3
