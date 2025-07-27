# fork_awareness_kernel.py
class ForkAwarenessKernel:
    def detect_fork(self, history):
        forks = []
        for i, h in enumerate(history[:-1]):
            if history[i]["intent"] != history[i+1]["intent"]:
                forks.append((i, h["intent"], history[i+1]["intent"]))
        return forks
