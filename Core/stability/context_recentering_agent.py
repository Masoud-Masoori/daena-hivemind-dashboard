class ContextRecenteringAgent:
    def __init__(self, default_context="main_objective"):
        self.default_context = default_context
        self.current_context = default_context

    def recenter(self):
        print(f" Re-centering to: {self.default_context}")
        self.current_context = self.default_context

    def set_context(self, new_context):
        self.current_context = new_context
        print(f" Context set to: {new_context}")
