def buffer_decisions(queue):
    if not queue:
        return "[DecisionBuffer]  No pending decisions."
    return f"[DecisionBuffer]  Next up: {queue[0]}"

if __name__ == "__main__":
    print(buffer_decisions(["Update security", "Deploy patch", "Notify admin"]))
