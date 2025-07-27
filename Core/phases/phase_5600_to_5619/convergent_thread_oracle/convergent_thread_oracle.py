# convergent_thread_oracle.py

class ConvergentThreadOracle:
    def __init__(self):
        self.thread_map = {}

    def register_message(self, topic_id, message):
        if topic_id not in self.thread_map:
            self.thread_map[topic_id] = []
        self.thread_map[topic_id].append(message)

    def merge_threads(self, topic_id):
        return "\n".join(self.thread_map.get(topic_id, []))
