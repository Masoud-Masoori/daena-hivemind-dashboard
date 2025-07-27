from datetime import datetime

def check_drift(current_time_str, last_time_str):
    fmt = "%Y-%m-%d %H:%M:%S"
    current_time = datetime.strptime(current_time_str, fmt)
    last_time = datetime.strptime(last_time_str, fmt)
    diff = abs((current_time - last_time).total_seconds())
    return diff > 600  # Flag if over 10 minutes drift
