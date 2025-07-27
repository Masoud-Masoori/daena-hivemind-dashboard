def log_freelance_outcome(task, revenue):
    with open("D:/Ideas/Daena/logs/freelance_outcomes.txt", "a") as log:
        log.write(f"{task}: ${revenue}\n")
    print(f" Logged freelance outcome: {task} earned ${revenue}")
