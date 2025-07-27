def recursive_belief(input, depth):
    if depth == 0:
        return input
    return recursive_belief(f"belief({input})", depth - 1)

if __name__ == "__main__":
    print("[Recursive Belief ]:", recursive_belief("data", 3))
