def sanity_check(agent_state):
    return agent_state in ["stable", "calm", "engaged"]

if __name__ == "__main__":
    print("[SanityCheck]  A1:", sanity_check("engaged"))
