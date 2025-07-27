def allow_execution(task_type, user_trust_score):
    if task_type in ["secure", "financial"] and user_trust_score < 0.8:
        return False
    return True

if __name__ == "__main__":
    print("[Execute Filter] ", allow_execution("secure", 0.6))
