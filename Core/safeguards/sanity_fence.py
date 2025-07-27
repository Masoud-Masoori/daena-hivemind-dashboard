def sanity_check(signal):
    return signal in ["OK", "STABLE", "SAFE"]

if __name__ == "__main__":
    print("[Sanity Status ]:", sanity_check("OK"))
