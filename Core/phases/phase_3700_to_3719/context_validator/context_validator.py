# context_validator.py
class ContextValidator:
    def __init__(self, memory_store):
        self.memory = memory_store

    def validate_context(self, incoming_context):
        for past_context in reversed(self.memory[-10:]):
            if past_context["topic"] == incoming_context["topic"]:
                return True
        return False
