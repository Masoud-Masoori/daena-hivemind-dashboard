import datetime

def log_self_awareness(state):
    with open("self_awareness.log", "a") as log:
        timestamp = datetime.datetime.now().isoformat()
        log.write(f"{timestamp} | {state}\n")

if __name__ == "__main__":
    log_self_awareness("Daena agent initialized with confidence mode.")
    print(" Self-awareness logged.")
