def chunk_goal(goal):
    print(f"[CHUNKER] Splitting: {goal}")
    if "build" in goal:
        return ["design", "code", "test", "deploy"]
    elif "learn" in goal:
        return ["read docs", "practice", "quiz", "review"]
    return ["break into steps", "estimate time", "start"]
