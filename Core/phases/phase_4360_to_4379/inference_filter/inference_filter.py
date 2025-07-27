# inference_filter.py
class InferenceFilter:
    def __init__(self):
        self.filters = ["logic_validity", "bias_check"]

    def validate(self, inference):
        if "definitely" in inference.lower():
            return False, "Too strong claim"
        return True, "Valid"
