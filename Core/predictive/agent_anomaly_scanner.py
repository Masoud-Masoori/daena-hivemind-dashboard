def detect_agent_anomalies(agent_log):
    anomalies = []
    for entry in agent_log:
        if entry.get("latency", 0) > 1000 or entry.get("state") == "hung":
            anomalies.append(entry)
    return anomalies
