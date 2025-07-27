from datetime import datetime

def log_event(event, timeline=[]):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timeline.append(f"{timestamp}  {event}")
    return timeline

if __name__ == "__main__":
    log = log_event("Initialized Daena Core")
    print(log_event("LLM Interaction Logged", log))
