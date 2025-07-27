def filter_emotion(response, level="medium"):
    tone = "[Emotion]  Filtered (soft)" if level == "low" else "[Emotion]  Filtered (firm)"
    return f"{tone} -> {response}"

if __name__ == "__main__":
    print(filter_emotion("Let's crush this!", level="high"))
