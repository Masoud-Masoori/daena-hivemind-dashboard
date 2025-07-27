import datetime

def log_lock_state(state):
    with open("meta_lock.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - Lock: {state}\\n")
