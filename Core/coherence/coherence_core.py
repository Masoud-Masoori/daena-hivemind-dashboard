def assess_coherence(segments):
    return "[CoherenceEngine]  Semantic alignment:" + " && ".join(segments)

if __name__ == "__main__":
    print(assess_coherence(["Greeting detected", "Task matched", "Agent response in sync"]))
