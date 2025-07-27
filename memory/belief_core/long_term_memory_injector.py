import os, json

def inject_decision_memory():
    memory_log = "D:/Ideas/Daena/memory/logs/decision_summary.json"
    injection_path = "D:/Ideas/Daena/memory/injected_long_term.json"

    if not os.path.exists(memory_log):
        print(" No decision summary found.")
        return

    with open(memory_log) as f:
        data = json.load(f)

    injected = {
        "long_term_summary": data[-50:] if isinstance(data, list) else []
    }

    with open(injection_path, "w") as f:
        json.dump(injected, f, indent=2)

    print(" Long-term memory injected.")
    
if __name__ == "__main__":
    inject_decision_memory()
