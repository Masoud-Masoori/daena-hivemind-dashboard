def scan_pulse(data_stream):
    threats = ["override", "leak", "escalation"]
    for d in data_stream:
        for threat in threats:
            if threat in d.lower():
                return f"THREAT DETECTED: {threat}"
    return "CLEAN"
