def scan_pulse_status(pulse_data):
    if pulse_data.get("rhythm") != "normal":
        return "anomaly"
    if pulse_data.get("latency", 0) > 0.5:
        return "delayed"
    return "stable"
