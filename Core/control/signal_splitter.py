def split_signal(departments, signal):
    return {dept: f"{signal}  {dept}" for dept in departments}

if __name__ == "__main__":
    result = split_signal(["LLM", "Security", "Finance"], "UpdatePolicy")
    print("[SignalSplitter] ", result)
