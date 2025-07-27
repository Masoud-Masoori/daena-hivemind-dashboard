class InterruptFlowRedirector:
    def __init__(self):
        self.cache = []

    def intercept(self, message):
        self.cache.append(message)
        print(f" Interrupt cached: {message}")
        return "Redirected for later processing"
