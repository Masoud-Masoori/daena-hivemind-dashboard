import os
import json
import time

def agent_diagnostics_report(output_file="core/diagnostics/agent_report.json"):
    report = {
        "time": time.ctime(),
        "agents_active": os.listdir("agents") if os.path.exists("agents") else [],
        "files_in_data": len(os.listdir("data")) if os.path.exists("data") else 0
    }
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    print("Agent diagnostics saved.")
