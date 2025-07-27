# divergence_memory_linker.py
class DivergenceMemoryLinker:
    def track_divergence(self, current_topic, user_input):
        if current_topic not in user_input:
            return {"diverged": True, "from": current_topic, "to": user_input}
        return {"diverged": False}
