def route_intent(intent, handlers):
    for h in handlers:
        if h.can_handle(intent):
            return h.handle(intent)
    return "No handler found for intent."
