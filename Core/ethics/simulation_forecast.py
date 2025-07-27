def simulate_scenario(risk, reward):
    if reward > risk:
        return "Proceed"
    else:
        return "Halt and escalate"

if __name__ == "__main__":
    print("[Simulation]:", simulate_scenario(2, 10))
