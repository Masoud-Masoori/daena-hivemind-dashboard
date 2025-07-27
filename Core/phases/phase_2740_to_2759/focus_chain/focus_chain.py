# focus_chain.py
import json
from datetime import datetime

FOCUS_FILE = "D:/Ideas/Daena/logs/focus_chain.json"

def append_focus_entry(step, status):
    data = {
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "status": status
    }
    try:
        with open(FOCUS_FILE, 'r') as f:
            chain = json.load(f)
    except:
        chain = []
    chain.append(data)
    with open(FOCUS_FILE, 'w') as f:
        json.dump(chain, f, indent=2)
    print(f"[FocusChain] Step '{step}' logged with status '{status}'")
