def check_high_risk_action(cost):
    if cost > 500:
        print(" CMP Alert: Action exceeds safe threshold. Awaiting approval.")
        return False
    return True
