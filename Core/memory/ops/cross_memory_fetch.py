def fetch_from_sources(sources):
    result = []
    for src in sources:
        result += src
    return result

if __name__ == "__main__":
    s1 = ["intro", "alignment"]
    s2 = ["mission", "ethics"]
    print("[MemoryFetch] ", fetch_from_sources([s1, s2]))
