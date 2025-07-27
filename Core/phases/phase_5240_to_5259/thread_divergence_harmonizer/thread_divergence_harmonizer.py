# thread_divergence_harmonizer.py
class ThreadDivergenceHarmonizer:
    def harmonize(self, threads):
        return sorted(set([msg for thread in threads for msg in thread]), key=lambda x: len(x))
