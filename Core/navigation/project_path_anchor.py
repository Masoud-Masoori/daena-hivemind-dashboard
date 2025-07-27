class ProjectAnchor:
    def __init__(self):
        self.anchor = None

    def set_anchor(self, objective):
        self.anchor = objective
        print(f" Anchor set: {objective}")

    def recall(self):
        return f" Returning to anchor point: {self.anchor}"
