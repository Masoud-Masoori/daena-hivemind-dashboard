import traceback

def trace_decision_flow():
    try:
        raise ValueError("Trigger Decision Chain")
    except Exception:
        return traceback.format_exc()

if __name__ == "__main__":
    print("[Traceback Hook ]:")
    print(trace_decision_flow())
