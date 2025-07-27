import time

def evaluate_stress_response(model, input_text):
    start = time.time()
    _ = model(input_text)
    duration = time.time() - start
    return f"[StressEval] Response Time: {duration:.3f}s"

if __name__ == "__main__":
    evaluate_stress_response(lambda x: x, "Run complex prompt")
