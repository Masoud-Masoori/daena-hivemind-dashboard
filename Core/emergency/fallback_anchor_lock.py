class FallbackAnchorLock:
    def __init__(self, anchor_point="core_directive"):
        self.anchor = anchor_point

    def enforce(self, current_focus):
        if current_focus != self.anchor:
            print(f" Redirecting focus back to anchor: {self.anchor}")
            return self.anchor
        print(" Focus is on anchor.")
        return current_focus
