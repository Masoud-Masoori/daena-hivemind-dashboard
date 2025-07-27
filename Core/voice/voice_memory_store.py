voice_memory = []

def store_voice_interaction(text, emotion, timestamp):
    global voice_memory
    voice_memory.append({"text": text, "emotion": emotion, "timestamp": timestamp})
    print(f"[VOICE MEMORY] Stored interaction at {timestamp}")
