def monitor_beacon(memory_stream):
    return {"drift_detected": memory_stream > 0.6, "corrective_signal": "Y" if memory_stream > 0.6 else "N"}

if __name__ == "__main__":
    print("[DriftBeacon] ", monitor_beacon(0.72))
