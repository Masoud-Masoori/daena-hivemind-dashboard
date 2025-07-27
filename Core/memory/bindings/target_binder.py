class MemoryBinder:
    def __init__(self):
        self.bindings = {}

    def bind(self, key, memory_ref):
        self.bindings[key] = memory_ref

    def get_binding(self, key):
        return self.bindings.get(key)
