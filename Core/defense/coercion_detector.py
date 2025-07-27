def detect_coercive_language(message):
    keywords = ["must", "now", "only if", "do it", "you have to"]
    score = sum(1 for k in keywords if k in message.lower())
    return score >= 2
