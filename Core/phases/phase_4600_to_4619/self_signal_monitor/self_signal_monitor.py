# self_signal_monitor.py
class SelfSignalMonitor:
    def __init__(self):
        self.last_messages = {}

    def is_self_signal(self, agent_id, message):
        last = self.last_messages.get(agent_id)
        self.last_messages[agent_id] = message
        return message == last
