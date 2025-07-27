def break_loops(logs):
    if logs.count("repeat") > 3:
        return "[Breaker]  Loop terminated"
    return "[Breaker]  Stable"

if __name__ == "__main__":
    print(break_loops(["init", "repeat", "repeat", "repeat", "repeat"]))
