# emotion_filter.py
def apply_emotion(text, emotion="neutral"):
    tones = {
        "neutral": text,
        "friendly": " " + text,
        "serious": " " + text,
        "angry": " " + text,
        "happy": " " + text,
        "sad": " " + text
    }
    return tones.get(emotion.lower(), text)
