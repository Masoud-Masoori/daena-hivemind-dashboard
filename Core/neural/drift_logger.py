def log_drift(timestamp, zone):
    return f"[NeuralDriftLog]  {timestamp}  {zone} misalignment detected"

if __name__ == "__main__":
    print(log_drift("2025-06-01T10:30:00", "hive_sync"))
