def reset_to_safe_state():
    return {
        "mode": "safe",
        "llm_status": "neutral",
        "decision_pending": True
    }

if __name__ == "__main__":
    print("[Reset]:", reset_to_safe_state())
