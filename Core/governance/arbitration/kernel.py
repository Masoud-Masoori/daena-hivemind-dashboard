class ArbitrationKernel:
    def __init__(self):
        self.handlers = []

    def register_handler(self, handler):
        self.handlers.append(handler)

    def resolve(self, conflict):
        for handler in self.handlers:
            result = handler(conflict)
            if result:
                return result
        return None
