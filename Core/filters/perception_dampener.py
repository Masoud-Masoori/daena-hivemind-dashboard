def dampen_perception(input_signal, sensitivity=0.5):
    result = "[Perception]  Dampened" if len(input_signal) * sensitivity < 10 else "[Perception]  Unaffected"
    return result

if __name__ == "__main__":
    print(dampen_perception("noisy input", sensitivity=0.3))
