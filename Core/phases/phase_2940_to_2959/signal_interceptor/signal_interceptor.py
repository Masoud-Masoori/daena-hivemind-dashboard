# signal_interceptor.py

def intercept(agent_id, message):
    if "[[INTERNAL]]" in message:
        print(f"[SignalInterceptor]  Internal message detected from {agent_id}: suppressed from public output.")
        return None
    print(f"[SignalInterceptor]  Message passed from {agent_id}")
    return message
