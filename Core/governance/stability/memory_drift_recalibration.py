def recalibrate_memory(drift_value):
    if abs(drift_value) > 0.7:
        return "[MEMORY]  Recalibration initiated"
    return "[MEMORY] Stable"

if __name__ == "__main__":
    print(recalibrate_memory(0.8))
