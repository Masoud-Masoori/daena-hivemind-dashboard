def run_safety_check(signal):
    if "threat" in signal:
        print(" Safety threat detected! Initiating protocols.")
    else:
        print(" Safety check passed.")
