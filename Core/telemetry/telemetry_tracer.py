from .telemetry_guard import secure_log

def trace_websocket_event(event_type: str, detail: str):
    secure_log(f"WebSocket {event_type}: {detail}", "telemetry_tracer")
