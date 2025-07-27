def preprocess_signal(signal):
    return f"[SignalPrep]  Cleaned: {signal.strip().lower()}"

if __name__ == "__main__":
    print(preprocess_signal("   WARNING: SYSTEM OVERLOAD   "))
