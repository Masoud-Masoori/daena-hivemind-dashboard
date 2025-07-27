import time
def monitor_uptime(last_active):
    now = time.time()
    if now - last_active > 120:
        print(" Downtime detected  agent inactive > 2 minutes.")
