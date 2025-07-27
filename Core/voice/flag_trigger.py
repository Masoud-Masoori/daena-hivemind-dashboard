def trigger_flag(intensity):
    return intensity > 0.9

if __name__ == "__main__":
    if trigger_flag(0.95):
        print("[VoiceFlag]  Raised for review")
    else:
        print("[VoiceFlag]  Normal range")
