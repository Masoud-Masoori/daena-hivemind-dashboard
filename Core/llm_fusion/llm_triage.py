def evaluate_responses(responses):
    ranked = sorted(responses, key=lambda r: r["confidence"], reverse=True)
    return ranked[0]["text"]

if __name__ == "__main__":
    test = [
        {"text": "Yes, that is correct.", "confidence": 0.85},
        {"text": "No, try another approach.", "confidence": 0.65},
        {"text": "Possibly, with more data.", "confidence": 0.73}
    ]
    print("[LLM Eval]  Chosen:", evaluate_responses(test))
