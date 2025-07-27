def narrative_memory(steps):
    return "[Narrative]  " + "  ".join(steps)

if __name__ == "__main__":
    print(narrative_memory(["met user", "learned context", "responded accordingly"]))
