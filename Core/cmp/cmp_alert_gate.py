def should_alert(event_type, cost):
    if event_type == "high-risk" or cost > 500:
        return True
    return False
