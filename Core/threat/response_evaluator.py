def evaluate_response(logs):
    severity = sum(1 for l in logs if "THREAT" in l)
    if severity > 3:
        return "ESCALATE"
    elif severity > 0:
        return "MONITOR"
    return "STANDBY"
