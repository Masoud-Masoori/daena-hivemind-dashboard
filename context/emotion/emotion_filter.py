# Filters LLM responses for emotional tone
def filter_emotion(text):
    import re
    happy_keywords = ["great", "love", "excited", "fantastic", "happy"]
    if any(word in text.lower() for word in happy_keywords):
        return "positive"
    return "neutral"
