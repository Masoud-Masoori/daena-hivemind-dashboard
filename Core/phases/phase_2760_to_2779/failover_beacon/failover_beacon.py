# failover_beacon.py

from datetime import datetime

def drop_beacon(event):
    stamp = datetime.now().isoformat()
    print(f"[Beacon]  Failover triggered at {stamp} due to: {event}")
    print("[Beacon] Broadcasting to agents... Updating control flow!")
