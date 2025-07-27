# Stores and re-invokes useful past commands
class CommandRecaller:
    def __init__(self):
        self.memory = []

    def remember(self, cmd):
        self.memory.append(cmd)

    def recall(self):
        return self.memory[-1] if self.memory else None
