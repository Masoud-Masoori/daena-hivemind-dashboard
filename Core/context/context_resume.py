class ContextResume:
    def __init__(self):
        self.last_context = None

    def save(self, context):
        self.last_context = context
        print(" Context saved.")

    def restore(self):
        print(" Restoring context...")
        return self.last_context
