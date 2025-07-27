def gate_drift(signal_strength):
    if signal_strength < 0.6:
        return "[DriftGate]  Blocked weak signal"
    return "[DriftGate]  Passed"

if __name__ == "__main__":
    print(gate_drift(0.55))
