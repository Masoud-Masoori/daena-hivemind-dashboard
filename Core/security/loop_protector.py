class LoopProtector:
    def __init__(self):
        self.count = 0
        self.limit = 100

    def ping(self):
        self.count += 1
        if self.count > self.limit:
            raise Exception("Loop detected and prevented.")
