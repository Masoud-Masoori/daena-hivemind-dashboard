class MindTrail:
    def __init__(self):
        self.history = []

    def log(self, step):
        self.history.append(step)

    def show(self):
        print(" Mind Trail:")
        for h in self.history:
            print(f" - {h}")
