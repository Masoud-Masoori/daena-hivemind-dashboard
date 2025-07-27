def map_emotions(history):
    amplified = {k: v.upper() + "!" for k, v in history.items()}
    return f"[EmoTrace]  {amplified}"

if __name__ == "__main__":
    print(map_emotions({"user": "calm", "agent": "neutral"}))
