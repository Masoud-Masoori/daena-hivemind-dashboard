def interpret_emotion(signal):
    mapping = {
        "": "anger",
        "": "sadness",
        "": "joy",
        "": "fear"
    }
    return mapping.get(signal, "neutral")

if __name__ == "__main__":
    print("[EmotionRouter] Interpreted:", interpret_emotion(""))
