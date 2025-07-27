def detect_interference(signal_data):
    if "noise" in signal_data.lower():
        print(" Signal interference detected!")
        return True
    return False
