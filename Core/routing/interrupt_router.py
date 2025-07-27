class InterruptRouter:
    def __init__(self, context_memory):
        self.context_memory = context_memory

    def handle_interrupt(self, cause):
        self.context_memory["last_interrupt"] = cause
        print(f" Interrupt detected: {cause}")
        return "redirecting_to_safe_state"
