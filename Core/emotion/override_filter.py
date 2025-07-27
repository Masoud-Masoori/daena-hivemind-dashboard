def override_emotion_if_critical(emotion, context_priority):
    if context_priority == "high" and emotion in ["fear", "hesitation"]:
        return "override"
    return emotion
