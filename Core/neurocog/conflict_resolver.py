def resolve_conflict(viewpoints):
    return max(set(viewpoints), key=viewpoints.count)

if __name__ == "__main__":
    print("[Conflict Resolver ]:", resolve_conflict(["agree", "disagree", "agree", "neutral"]))
