def detect_stress(inputs):
    alert = [i for i in inputs if "!!!" in i]
    return f"[StressDetector]  {len(alert)} stress signals"

if __name__ == "__main__":
    print(detect_stress(["okay", "problem!!!", "handled", "critical!!!"]))
