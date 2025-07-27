def detect_fork_activity(authority_branches):
    return any("unauthorized" in b.lower() for b in authority_branches)

if __name__ == "__main__":
    branches = ["MainOps", "DevStream", "UnauthorizedPatch"]
    print("[ForkDetector]  Alert!" if detect_fork_activity(branches) else "[ForkDetector]  Clean.")
