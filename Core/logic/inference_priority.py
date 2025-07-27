def prioritize_task(task_type):
    priority = {
        "security": 1,
        "response": 2,
        "fetch": 3,
        "search": 4,
        "joke": 10
    }
    return priority.get(task_type, 5)

if __name__ == "__main__":
    print("[Prioritizer]  Level:", prioritize_task("security"))
