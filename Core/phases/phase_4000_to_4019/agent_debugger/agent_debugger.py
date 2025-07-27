# agent_debugger.py
class AgentDebugger:
    def __init__(self):
        self.logs = []

    def log(self, message, agent_name):
        self.logs.append({"agent": agent_name, "message": message})

    def review_logs(self, agent_name=None):
        if agent_name:
            return [log for log in self.logs if log["agent"] == agent_name]
        return self.logs
