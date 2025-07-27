# meta_awareness_hook.py

def check_meta_awareness(agent_id, context_stack):
    if len(context_stack) > 15:
        print(f"[MetaAwareness]  Agent {agent_id} may be overthinking  truncating past context.")
        return context_stack[-10:]
    print(f"[MetaAwareness]  Agent {agent_id} meta-state is stable.")
    return context_stack
