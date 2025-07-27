class AgentThreadSync:
    def __init__(self):
        self.active_threads = []

    def register_thread(self, agent_id, task_id):
        self.active_threads.append((agent_id, task_id))
        print(" Agent thread registered.")

    def sync_status(self):
        return self.active_threads
