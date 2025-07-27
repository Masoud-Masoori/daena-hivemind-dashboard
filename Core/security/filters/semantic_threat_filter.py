def filter_threats(text):
    flagged_words = ["exploit", "attack", "override"]
    if any(word in text.lower() for word in flagged_words):
        return "[ThreatFilter]  Threat Detected"
    return "[ThreatFilter]  Safe"

if __name__ == "__main__":
    print(filter_threats("Please override the system."))
