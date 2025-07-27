def reconstruct_chain(thoughts):
    return " -> ".join(thoughts)

if __name__ == "__main__":
    thoughts = ["Identify goal", "Check options", "Select best path"]
    print("[ReasonChain] " + reconstruct_chain(thoughts))
