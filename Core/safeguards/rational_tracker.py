def track_rationale(rationale):
    return [r for r in rationale if "because" in r]

if __name__ == "__main__":
    rlog = ["action because data", "skip", "redirect because user request"]
    print("[Rational Logs ]:", track_rationale(rlog))
