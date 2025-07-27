def alert_cascade(level):
    alerts = []
    for i in range(level):
        alerts.append(f"ALERT-{i+1}")
    return alerts
