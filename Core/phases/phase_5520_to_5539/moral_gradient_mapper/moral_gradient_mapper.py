# moral_gradient_mapper.py

class MoralGradientMapper:
    def __init__(self):
        self.spectrum = {
            "selfish": -1,
            "neutral": 0,
            "altruistic": 1
        }

    def map_decision(self, action):
        score = self.spectrum.get(action.lower(), 0)
        return f"Action '{action}' has moral gradient: {score}"
