def detect_sentiment_drift(current_sentiment, baseline="neutral"):
    if current_sentiment != baseline:
        print(f" Drift detected: {current_sentiment} vs {baseline}")
        return True
    return False
