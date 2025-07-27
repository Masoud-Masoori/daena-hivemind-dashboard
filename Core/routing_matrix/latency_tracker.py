import time

def track_latency(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return f"[Latency]  {end - start:.3f}s - {result}"
    return wrapper

@track_latency
def fake_call():
    time.sleep(0.1)
    return "Processed."

if __name__ == "__main__":
    print(fake_call())
