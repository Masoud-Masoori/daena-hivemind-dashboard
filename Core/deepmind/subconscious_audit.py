def log_subconscious(events):
    return [e for e in events if "impulse" in e or "reflex" in e]

if __name__ == "__main__":
    impulses = ["reflex_jump", "thought_delay", "impulse_stop"]
    print("[SubAudit ]:", log_subconscious(impulses))
