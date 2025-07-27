def detect_leakage(response, user_identity):
    if user_identity.lower() in response.lower():
        return "[LeakageDetector] Potential leak detected!"
    return "[LeakageDetector] Safe."

if __name__ == "__main__":
    print(detect_leakage("Hello Masoud, here is your info.", "Masoud"))
