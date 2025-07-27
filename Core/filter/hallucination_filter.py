def detect_hallucination(response, sources):
    for src in sources:
        if src.lower() in response.lower():
            return False
    return True  # Assume hallucination if unmatched
