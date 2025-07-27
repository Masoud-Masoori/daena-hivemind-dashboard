def bounce_sentiment(feedback):
    if "hate" in feedback.lower() or "fail" in feedback.lower():
        return "[Bounce]  Rejected toxic feedback"
    return "[Bounce]  Accepted"

if __name__ == "__main__":
    print(bounce_sentiment("I hate this"))
