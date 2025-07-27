# replay_viewer.py

def replay_conversation(trace_log):
    for i, step in enumerate(trace_log):
        print(f"Step {i+1}:")
        print(f"User: {step['user']}")
        print(f"Daena: {step['daena']}")
        print("-" * 40)
