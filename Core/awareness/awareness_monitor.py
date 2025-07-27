def monitor_awareness(signal_data):
    if "disoriented" in signal_data.lower():
        print("Awareness anomaly detected.")
        return True
    return False
