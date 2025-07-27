def validate_memory(entry):
    return entry.strip().endswith(".")

if __name__ == "__main__":
    print("[Memory Validator ]:", validate_memory("Daena remembered."))
