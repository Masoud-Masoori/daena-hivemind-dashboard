def verify_integrity(dialogue):
    return all(isinstance(line, str) and line.strip() != "" for line in dialogue)

if __name__ == "__main__":
    valid = verify_integrity(["Hi", "How are you?", "Ready to proceed."])
    print(f"[IntegrityVerifier]  Valid: {valid}")
