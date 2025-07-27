def deviation_guard(memory_hash, current_hash):
    if memory_hash != current_hash:
        return "[MemoryGuard]  Drift detected!"
    return "[MemoryGuard]  Memory stable"

if __name__ == "__main__":
    print(deviation_guard("abc123", "abc123"))
