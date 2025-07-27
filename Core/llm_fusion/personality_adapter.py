def apply_personality(response, tone="warm", style="insightful"):
    return f"[{tone.upper()} / {style.upper()}] {response}"

if __name__ == "__main__":
    print("[Personality] ", apply_personality("Let me help you with that."))
