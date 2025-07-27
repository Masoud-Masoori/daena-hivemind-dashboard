# thread_stitcher.py
class ThreadStitcher:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def stitch(self):
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])
