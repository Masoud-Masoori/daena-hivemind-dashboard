def track_divergence(expected, actual):
    return {"diverged": expected != actual, "expected": expected, "actual": actual}

if __name__ == "__main__":
    print("[Divergence] ", track_divergence("Approve", "Reject"))
