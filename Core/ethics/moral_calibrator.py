def calibrate_response(response):
    weights = {"protect life": 10, "privacy": 8, "freedom": 6}
    score = sum(weights.get(k, 0) for k in weights if k in response.lower())
    return f"[MoralCalibrator] Moral Score = {score}"

if __name__ == "__main__":
    print(calibrate_response("This decision protects life and privacy."))
