# agent_threads.py
import threading
import time

class AgentThreadManager:
    def __init__(self):
        self.threads = {}

    def start_agent(self, agent_id, task_fn):
        if agent_id in self.threads:
            print(f"Agent {agent_id} already running.")
            return
        thread = threading.Thread(target=task_fn, daemon=True)
        self.threads[agent_id] = thread
        thread.start()

    def is_alive(self, agent_id):
        return self.threads.get(agent_id, None).is_alive() if agent_id in self.threads else False
