def harmonize(dialogues):
    return "[Harmonizer]  " + " | ".join(sorted(set(dialogues)))

if __name__ == "__main__":
    print(harmonize(["agent_a: hello", "agent_b: hi", "agent_a: hello"]))
