def prioritize_thoughts(thoughts):
    return sorted(thoughts, key=lambda t: len(t), reverse=True)

if __name__ == "__main__":
    print(prioritize_thoughts(["short", "much longer thought", "mid-size"]))
