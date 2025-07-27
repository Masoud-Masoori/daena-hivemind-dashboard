def filter_intensity(level):
    if level > 0.85:
        return "[VoiceFilter]  Suppressed  too intense"
    elif level < 0.1:
        return "[VoiceFilter]  Boosted  too quiet"
    return "[VoiceFilter]  Normalized"

if __name__ == "__main__":
    print(filter_intensity(0.9))
