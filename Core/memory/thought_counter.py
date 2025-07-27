_counter = 0

def next_thought_id():
    global _counter
    _counter += 1
    return f"THX-{_counter:05d}"

if __name__ == "__main__":
    print("[ThoughtID] ", next_thought_id())
