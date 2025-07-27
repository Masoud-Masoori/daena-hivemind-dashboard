# interrupt_resolver.py
class InterruptResolver:
    def __init__(self):
        self.interrupt_buffer = {}

    def register_interrupt(self, agent_id, context):
        self.interrupt_buffer[agent_id] = context

    def resolve_interrupt(self, agent_id):
        return self.interrupt_buffer.pop(agent_id, "No interrupt registered.")
