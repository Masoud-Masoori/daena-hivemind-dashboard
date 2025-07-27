def mirror_prediction(actual, predicted):
    error_margin = abs(actual - predicted)
    return f"[PredictMirror] Actual: {actual}, Predicted: {predicted}, Error: {error_margin}"

if __name__ == "__main__":
    print(mirror_prediction(0.92, 0.87))
