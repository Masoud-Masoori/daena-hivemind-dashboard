# inner_world_synthesizer.py
class InnerWorldSynthesizer:
    def __init__(self):
        self.internal_state = {}

    def simulate(self, context):
        self.internal_state["emotion"] = "curious" if "?" in context else "neutral"
        self.internal_state["attention"] = "high" if len(context) > 200 else "normal"
        return self.internal_state
