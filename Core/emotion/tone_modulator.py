def modulate_emotion(text, level="neutral"):
    if level == "warm":
        return " " + text
    elif level == "serious":
        return " " + text
    return text
