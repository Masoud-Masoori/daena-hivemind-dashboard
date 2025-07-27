def predict_intent(previous):
    keywords = [p.split()[0] for p in previous if p]
    return f"[Prediction]  Next likely action: {keywords[-1]}-refine"

if __name__ == "__main__":
    print(predict_intent(["ask question", "get data", "analyze response"]))
