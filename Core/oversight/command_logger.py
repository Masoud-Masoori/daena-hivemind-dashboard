import datetime

def log_command(command):
    timestamp = datetime.datetime.now().isoformat()
    return f"[Log]  {timestamp} - Command Executed: {command}"

if __name__ == "__main__":
    print(log_command("Run cross-department sync"))
