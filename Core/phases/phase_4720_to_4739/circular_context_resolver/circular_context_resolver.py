# circular_context_resolver.py
class CircularContextResolver:
    def __init__(self):
        self.previous_contexts = []

    def resolve(self, context):
        if context in self.previous_contexts:
            return "Loop detected. Adjusting response strategy."
        self.previous_contexts.append(context)
        return context
