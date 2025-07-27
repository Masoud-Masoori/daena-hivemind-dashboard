def monitor_load(cpu, memory):
    if cpu > 90 or memory > 90:
        return " Overload Detected"
    return " Normal Operation"

if __name__ == "__main__":
    print("[System Load ]:", monitor_load(87, 65))
