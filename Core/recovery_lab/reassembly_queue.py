class MindQueue:
    def __init__(self):
        self.queue = []
    def add(self, piece): self.queue.append(piece)
    def assemble(self): return "[Reassembly]  " + " + ".join(self.queue)

if __name__ == "__main__":
    q = MindQueue()
    q.add("short-term")
    q.add("memory")
    print(q.assemble())
