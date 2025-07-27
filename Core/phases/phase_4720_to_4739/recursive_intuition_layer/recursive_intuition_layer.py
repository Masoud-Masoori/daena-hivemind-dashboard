# recursive_intuition_layer.py
class RecursiveIntuitionLayer:
    def __init__(self):
        self.memory = []

    def guess_intent(self, message):
        if "how" in message.lower():
            return "Instructional"
        elif "why" in message.lower():
            return "Explanation"
        else:
            return "Response"
