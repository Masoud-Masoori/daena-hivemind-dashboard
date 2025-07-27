class StateReweaver:
    def __init__(self):
        self.fragments = []

    def reweave(self, fragments):
        self.fragments = fragments
        state = " > ".join(fragments)
        print(f" State re-woven: {state}")
        return state
