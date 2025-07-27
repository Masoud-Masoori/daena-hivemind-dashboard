import random

def regulate_emotion(text, level="calm"):
    if level == "excited":
        return text.upper() + "!! "
    elif level == "firm":
        return " " + text
    return text
