# FIXED WebSocket trace logging
def trace_websocket_event(event_type: str, details: str):
    print(f"[TRACE] WebSocket Event: {event_type}  {details}")

# Ensure this is called like:
trace_websocket_event("connect", "WebSocket opened")
