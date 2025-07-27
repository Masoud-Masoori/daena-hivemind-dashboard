class DistractionBlocker:
    def __init__(self):
        self.blocked = []

    def block(self, tag):
        self.blocked.append(tag)
        print(f" Distraction blocked: {tag}")

    def is_blocked(self, tag):
        return tag in self.blocked
