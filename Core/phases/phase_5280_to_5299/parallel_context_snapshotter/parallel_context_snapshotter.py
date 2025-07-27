# parallel_context_snapshotter.py
class ParallelContextSnapshotter:
    def snapshot(self, contexts):
        return [{"thread_id": i, "context": ctx} for i, ctx in enumerate(contexts)]
