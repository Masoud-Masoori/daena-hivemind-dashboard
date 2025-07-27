class CommandChain:
    def __init__(self):
        self.layers = ["Guardian", "HiveControl", "DaenaCore"]

    def escalate(self, level):
        if level < len(self.layers):
            return f"Escalated to: {self.layers[level]}"
        return "Invalid level"

if __name__ == "__main__":
    chain = CommandChain()
    print(chain.escalate(1))  # Escalate to HiveControl
