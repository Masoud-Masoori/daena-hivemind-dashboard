# emotional_depth_simulator.py

class EmotionalDepthSimulator:
    def __init__(self):
        self.emotional_palette = ["joy", "fear", "hope", "anger", "love", "sadness"]

    def simulate(self, stimulus):
        return f"Emotional response to '{stimulus}': {self.emotional_palette[hash(stimulus) % len(self.emotional_palette)]}"
