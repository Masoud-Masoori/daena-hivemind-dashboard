def block_drift(current_topic, mission):
    return mission.lower() in current_topic.lower()
