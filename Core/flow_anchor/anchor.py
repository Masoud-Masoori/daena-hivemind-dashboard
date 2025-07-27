class FlowAnchor:
    def __init__(self):
        self.anchor = None

    def set_anchor(self, focus_point):
        self.anchor = focus_point
        print(f" Anchor set to: {focus_point}")

    def get_anchor(self):
        return self.anchor or "No anchor set"
