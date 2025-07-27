# neural_adjuster.py
class NeuralAdjuster:
    def __init__(self):
        self.weights = {}

    def adjust_weight(self, key, delta):
        self.weights[key] = self.weights.get(key, 0.0) + delta
        print(f"[NeuralAdjuster] {key} adjusted by {delta}, new value: {self.weights[key]}")

    def reset_weights(self):
        self.weights.clear()
        print("[NeuralAdjuster] All weights reset.")
