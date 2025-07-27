from datetime import datetime

def temporal_reasoning(event_time_str):
    now = datetime.utcnow()
    event_time = datetime.fromisoformat(event_time_str)
    delta = now - event_time
    return f"Time delta: {delta.total_seconds()}s"

if __name__ == "__main__":
    print("[Temporal] ", temporal_reasoning("2025-05-30T20:00:00"))
