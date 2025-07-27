def sync_emotion(agent_emotion, user_emotion):
    return agent_emotion if agent_emotion == user_emotion else "neutral"

if __name__ == "__main__":
    print("[Emotion Sync] ", sync_emotion("happy", "frustrated"))
