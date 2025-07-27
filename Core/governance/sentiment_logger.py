def log_sentiment_effect(event, sentiment):
    return f"[SentimentLog]  Event: '{event}'  Influence: {sentiment}"

if __name__ == "__main__":
    print(log_sentiment_effect("customer query escalation", "empathy boost"))
