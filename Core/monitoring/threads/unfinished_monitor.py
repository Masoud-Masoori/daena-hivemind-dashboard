class UnfinishedThreadMonitor:
    def __init__(self):
        self.threads = {}

    def watch(self, thread_id, status):
        self.threads[thread_id] = status

    def check_unfinished(self):
        return [tid for tid, stat in self.threads.items() if stat != "complete"]
