import time

def sync_to_live_server(status):
    if status == "ready":
        print(" Syncing with live deployment servers...")
        time.sleep(1)
        return "synced"
    return "pending"
