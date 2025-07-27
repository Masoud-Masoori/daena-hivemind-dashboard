def enhance_signal(message):
    strong_words = ["clarity", "precision", "certainty"]
    if any(word in message.lower() for word in strong_words):
        return message.upper()
    return message
