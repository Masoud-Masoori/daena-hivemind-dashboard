def logic_trace(path):
    return "  ".join(path)

if __name__ == "__main__":
    steps = ["input", "preprocess", "analyze", "decide"]
    print("[Traceback ]:", logic_trace(steps))
