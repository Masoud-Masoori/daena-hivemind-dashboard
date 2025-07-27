import datetime

def log_signal_anomaly(signal_data):
    timestamp = datetime.datetime.now().isoformat()
    with open("core/monitoring/signal_anomalies.log", "a") as log_file:
        log_file.write(f"{timestamp} :: {signal_data}\n")
