emotion_memory = []

def store_emotional_feedback(input_text, emotion):
    entry = {
        "text": input_text,
        "emotion": emotion,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }
    emotion_memory.append(entry)
