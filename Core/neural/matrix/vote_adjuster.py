def adjust_weights(base, modifiers):
    return {k: base[k] * modifiers.get(k, 1.0) for k in base}

if __name__ == "__main__":
    weights = adjust_weights({"Qwen": 0.5, "R2": 0.8, "Yi": 0.7}, {"R2": 1.1})
    print("[Vote Weights Adjusted]", weights)
