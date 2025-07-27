def resolve_dispute(votes):
    decision = max(set(votes), key = votes.count)
    return {"votes": votes, "final_decision": decision}

if __name__ == "__main__":
    outcome = resolve_dispute(["Qwen", "R2", "Qwen", "Yi"])
    print("[Resolution Probe] Outcome:", outcome)
