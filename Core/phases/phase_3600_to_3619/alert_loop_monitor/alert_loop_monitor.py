# alert_loop_monitor.py
def track_alerts(logs, keyword="misalign"):
    return [line for line in logs if keyword.lower() in line.lower()]
