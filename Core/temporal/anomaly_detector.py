def detect_anomalies(trace):
    return "[Anomaly]  Detected" if "??? anomaly" in trace else "[Anomaly]  Clear"

if __name__ == "__main__":
    print(detect_anomalies("conversation normal  ??? anomaly  halt"))
