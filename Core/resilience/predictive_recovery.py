def predict_and_recover(signal):
    if "unstable" in signal.lower():
        return "[Predictor]  Recovery pattern initiated"
    return "[Predictor]  Stable"

if __name__ == "__main__":
    print(predict_and_recover("unstable feedback"))
