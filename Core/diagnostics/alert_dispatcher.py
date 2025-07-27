def dispatch_alert(agent_id, error_code):
    print(f"[ALERT] Agent {agent_id} reports issue: {error_code}")
    return f"alert_sent_{agent_id}"
