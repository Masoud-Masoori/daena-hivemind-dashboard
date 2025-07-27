def log_recovery(agent_name, skill_name):
    with open("D:/Ideas/Daena/logs/recovery_log.txt", "a") as log:
        log.write(f"{agent_name} recovered {skill_name}\n")
    print("Recovery logged.")
