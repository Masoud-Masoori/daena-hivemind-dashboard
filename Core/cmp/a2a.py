class A2AChannel:
    def __init__(self):
        self.connections = {}

    def connect(self, agentA, agentB):
        self.connections.setdefault(agentA, []).append(agentB)

    def broadcast(self, sender, msg):
        for target in self.connections.get(sender, []):
            print(f"[A2A] {sender}  {target}: {msg}")

a2a = A2AChannel()
