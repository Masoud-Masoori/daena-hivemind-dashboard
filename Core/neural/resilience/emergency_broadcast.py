def emergency_signal(code, message):
    return f"[EMERGENCY-{code}]  {message}"

if __name__ == "__main__":
    print(emergency_signal(302, "Agent fallback triggered"))
