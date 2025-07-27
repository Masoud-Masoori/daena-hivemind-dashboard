# optimizer.py
class ThoughtOptimizer:
    def refine(self, thoughts):
        unique_thoughts = list(set(thoughts))
        ranked = sorted(unique_thoughts, key=lambda t: -len(t))  # Rank by length or complexity
        return ranked[:5]
