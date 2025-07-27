def sanity_scan(thoughts):
    return all(isinstance(t, str) and len(t) < 200 for t in thoughts)

if __name__ == "__main__":
    print("[Sanity Layer ]:", sanity_scan(["Checking phase.", "All logic seems sound."]))
