class DecisionTunnel:
    def __init__(self):
        self.packets = []

    def send(self, packet):
        print(f"Sending decision packet: {packet}")
        self.packets.append(packet)

    def receive(self):
        if self.packets:
            return self.packets.pop(0)
        return None
