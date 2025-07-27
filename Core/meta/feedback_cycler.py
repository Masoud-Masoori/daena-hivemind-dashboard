def feedback_cycle(steps):
    for i, step in enumerate(steps, 1):
        print(f"[Cycle {i}] {step}")

if __name__ == "__main__":
    feedback_cycle(["R1 advises", "User input noted", "System reconsidered"])
