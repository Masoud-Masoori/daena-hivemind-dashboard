def reinforce(state):
    return "boosted" if state == "low" else "maintained"

if __name__ == "__main__":
    print("[Reinforcement ]:", reinforce("low"))
