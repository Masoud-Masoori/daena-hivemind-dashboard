def reflect_emotion(agent_id, emotion):
    print(f"[Emotion] Agent {agent_id} shows {emotion}")
    if emotion in ["anger", "confusion"]:
        return "flagged"
    return "clear"
