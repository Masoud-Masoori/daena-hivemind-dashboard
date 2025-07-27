class ContextualAnchor:
    def __init__(self):
        self.last_context = None

    def set_context(self, label):
        print(f" Anchored context: {label}")
        self.last_context = label

    def get_context(self):
        return self.last_context or "No anchor set."
