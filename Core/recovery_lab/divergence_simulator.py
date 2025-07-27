import random

def simulate_divergence(seed):
    variants = [f"{seed}_hypothesis_{i}" for i in range(3)]
    return "[Divergence]  " + ", ".join(variants)

if __name__ == "__main__":
    print(simulate_divergence("strategic_response"))
