# echo_shield.py
class EchoShield:
    def __init__(self):
        self.last_messages = {}

    def block_repeats(self, agent_id, message):
        if self.last_messages.get(agent_id) == message:
            return False  # Detected echo
        self.last_messages[agent_id] = message
        return True
