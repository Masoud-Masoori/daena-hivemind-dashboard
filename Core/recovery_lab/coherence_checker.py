def validate_threads(threads):
    return "[Coherence] " if all(threads) else "[Coherence] "

if __name__ == "__main__":
    print(validate_threads(["ok", "fine", "stable"]))
