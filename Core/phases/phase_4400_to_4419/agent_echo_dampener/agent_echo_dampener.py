# agent_echo_dampener.py
class AgentEchoDampener:
    def __init__(self):
        self.recent_messages = set()

    def should_suppress(self, message):
        if message in self.recent_messages:
            return True
        self.recent_messages.add(message)
        if len(self.recent_messages) > 50:
            self.recent_messages.pop()
        return False
