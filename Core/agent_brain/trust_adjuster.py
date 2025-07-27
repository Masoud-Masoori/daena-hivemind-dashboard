def adjust_trust(agent_name, score, success):
    trust = score + (1 if success else -1)
    return f"[Trust]  {agent_name}  New Trust Level: {trust}"

if __name__ == "__main__":
    print(adjust_trust("Agent_X", 7, False))
