def throttle_actions(actions, limit):
    return actions[:limit]

if __name__ == "__main__":
    print(throttle_actions(["a", "b", "c", "d", "e"], 3))
