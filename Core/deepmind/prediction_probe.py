def override_check(pred, actual):
    return pred != actual

if __name__ == "__main__":
    print("[Override Probe ]:", override_check("yes", "no"))
