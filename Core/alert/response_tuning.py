alert_settings = {
    "intrusion": "high",
    "resource_exhaustion": "medium",
    "low_priority_ping": "low"
}

def tune_alert(level):
    return alert_settings.get(level, "medium")
