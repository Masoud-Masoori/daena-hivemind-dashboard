# empathy_layer.py
class EmpathyLayer:
    def wrap_with_empathy(self, message, context="general"):
        if context == "support":
            return f"I understand that this might be frustrating. {message}"
        elif context == "celebration":
            return f"That's wonderful to hear! {message}"
        return f"I appreciate you sharing that. {message}"
