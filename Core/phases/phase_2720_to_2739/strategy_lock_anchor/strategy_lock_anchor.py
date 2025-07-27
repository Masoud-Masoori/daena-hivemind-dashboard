# strategy_lock_anchor.py
ANCHOR_FILE = "D:/Ideas/Daena/memory/anchor_mission.txt"

def lock_current_strategy(note):
    with open(ANCHOR_FILE, 'w') as f:
        f.write(note)
    print(f"[StrategyAnchor] Locked strategy note: {note}")

def recall_strategy():
    try:
        with open(ANCHOR_FILE, 'r') as f:
            print(f"[StrategyAnchor] Current locked strategy: {f.read()}")
    except:
        print("[StrategyAnchor] No locked strategy found.")
