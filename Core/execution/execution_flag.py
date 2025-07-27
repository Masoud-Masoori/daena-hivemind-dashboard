class ExecutionFlag:
    def __init__(self):
        self.flags = {}

    def set_flag(self, phase, status):
        self.flags[phase] = status
        print(f" Phase '{phase}' marked as: {status}")

    def get_flag(self, phase):
        return self.flags.get(phase, " Not marked")
