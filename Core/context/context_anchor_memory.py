class ContextAnchorMemory:
    def __init__(self):
        self.anchor = None

    def update_anchor(self, goal):
        print(f" Anchoring to: {goal}")
        self.anchor = goal

    def recall(self):
        return self.anchor
