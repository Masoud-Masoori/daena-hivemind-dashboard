def predict_and_heal(anomaly):
    if anomaly.get("latency", 0) > 1000:
        print("Predicting fix: throttle or optimize calls")
        return "optimize_latency"
    elif anomaly.get("state") == "hung":
        print("Predicting fix: reboot agent")
        return "restart_agent"
    return "monitor"
