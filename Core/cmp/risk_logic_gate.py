def check_risk(action):
    if action["risk_level"] > 7:
        print(" High-risk action detected. Awaiting user confirmation...")
        return False
    return True
