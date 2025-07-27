def catch_intent_shift(history):
    if history and history[-1] != "aligned":
        return f"[IntentCatch]  Misalignment detected: {history[-1]}"
    return "[IntentCatch]  Aligned"

if __name__ == "__main__":
    logs = ["aligned", "adjusted", "drifting"]
    for log in logs:
        print(catch_intent_shift(["aligned", log]))
