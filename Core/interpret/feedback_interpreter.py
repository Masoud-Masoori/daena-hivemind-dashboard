def interpret_feedback(feedback):
    tone = "Positive" if "good" in feedback.lower() else "Neutral"
    return f"[Feedback]  Interpreted as: {tone}  '{feedback.strip()}'"

if __name__ == "__main__":
    print(interpret_feedback("System response time is good"))
