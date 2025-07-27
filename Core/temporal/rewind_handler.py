class RewindHandler:
    def __init__(self):
        self.history = []

    def remember(self, step):
        self.history.append(step)

    def rewind(self, steps=1):
        return self.history[-steps:]

if __name__ == "__main__":
    rh = RewindHandler()
    rh.remember("Define hypothesis")
    rh.remember("Validate response")
    rh.remember("Cross-check")
    print(rh.rewind(2))
