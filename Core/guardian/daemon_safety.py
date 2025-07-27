import time

def safety_watch(task_time, timeout=10):
    if task_time > timeout:
        return "[Daemon]  Timeout triggered"
    return "[Daemon]  Within safe limit"

if __name__ == "__main__":
    print(safety_watch(12))
