def tune_gate(signal):
    if max(signal) - min(signal) > 0.5:
        return "GATE_TUNED"
    return "NO_ADJUSTMENT"
