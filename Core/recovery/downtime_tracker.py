downtime_log = []

def log_downtime(agent, timestamp):
    downtime_log.append((agent, timestamp))
    print(f"Downtime recorded for agent {agent} at {timestamp}")
