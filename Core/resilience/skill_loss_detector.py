def detect_skill_loss(logs):
    critical_terms = ["forgot", "unable", "missing"]
    for term in critical_terms:
        if term in logs.lower():
            print("Detected possible skill degradation.")
            return True
    return False
