_cache = {}

def store(key, value):
    _cache[key] = value
    return f"[Cache]  Stored key: {key}"

def retrieve(key):
    return _cache.get(key, "[Cache]  Not found")

if __name__ == "__main__":
    print(store("model", "R2"))
    print(retrieve("model"))
