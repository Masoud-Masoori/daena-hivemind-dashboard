def track_confidence(values):
    return {k: f"{v*100:.2f}%" for k, v in values.items()}

if __name__ == "__main__":
    conf = {"Qwen": 0.82, "R2": 0.91, "Yi": 0.76}
    print("[Confidence Tracker]", track_confidence(conf))
