import json, datetime

def log_task_feedback(task_type, score, llm, dept, time_spent):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "task": task_type,
        "score": score,
        "llm": llm,
        "department": dept,
        "duration": time_spent
    }
    with open("D:\\Ideas\\Daena\\logs\\training_feedback.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\\n")

# Example
log_task_feedback("customer_response", 8.5, "DeepSeek-R2", "ClientOps", 12)
