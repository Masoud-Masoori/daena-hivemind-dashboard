def pulse_signal(data):
    return {"status": "stable" if max(data) < 0.8 else "overload"}

if __name__ == "__main__":
    print("[Pulse Tracker ]:", pulse_signal([0.2, 0.3, 0.6]))
