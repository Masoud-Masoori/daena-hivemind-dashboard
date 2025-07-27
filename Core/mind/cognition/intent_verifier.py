def verify_intent(user_input):
    keywords = ["help", "stop", "launch", "report"]
    matched = [k for k in keywords if k in user_input.lower()]
    return {"intent_detected": bool(matched), "matches": matched}

if __name__ == "__main__":
    print("[Intent Check] ", verify_intent("launch the protocol"))
