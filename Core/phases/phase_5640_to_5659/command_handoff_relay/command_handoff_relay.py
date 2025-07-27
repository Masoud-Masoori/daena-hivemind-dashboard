# command_handoff_relay.py

class CommandHandoffRelay:
    def __init__(self):
        self.relay_queue = []

    def register_command(self, command, delegate_to):
        self.relay_queue.append({"cmd": command, "delegate": delegate_to})

    def handoff(self):
        if self.relay_queue:
            return self.relay_queue.pop(0)
        return None
