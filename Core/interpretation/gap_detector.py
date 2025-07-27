def detect_reasoning_gap(conversation):
    if "..." in conversation:
        return "[GapDetector] Gap found: triggering patch"
    return "[GapDetector] No gap detected"

if __name__ == "__main__":
    print(detect_reasoning_gap("User said... then changed topic."))
