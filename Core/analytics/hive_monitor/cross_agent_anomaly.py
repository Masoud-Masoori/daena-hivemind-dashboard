def anomaly_tracker(agent_logs):
    return [log for log in agent_logs if "anomaly" in log.lower()]

if __name__ == "__main__":
    logs = ["Normal operation", "anomaly detected in Qwen2", "heartbeat"]
    print("[AnomalyTracker] ", anomaly_tracker(logs))
