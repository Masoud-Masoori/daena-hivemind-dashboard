def verify_clone(identity_hash, known_hashes):
    if identity_hash in known_hashes:
        return "[CloneCheck]  Authentic Daena core"
    return "[CloneCheck]  Possible tampered clone"

if __name__ == "__main__":
    print(verify_clone("abc123", ["xyz789", "abc123"]))
