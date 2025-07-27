class ReRoutingSentinel:
    def __init__(self):
        self.history = []

    def analyze(self, input_stream):
        if "divert" in input_stream:
            print(" Divergence detected. Initiating re-route...")
            self.history.append(input_stream)
            return True
        return False
