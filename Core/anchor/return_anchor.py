class ReturnAnchor:
    def __init__(self):
        self.anchor_phase = None

    def set_anchor(self, phase):
        self.anchor_phase = phase

    def return_to_anchor(self):
        print(f" Returning to anchored phase: {self.anchor_phase}")
        return self.anchor_phase
