def multiplex_tasks(task_sets):
    output = []
    for prio, tasks in sorted(task_sets.items(), reverse=True):
        output.extend([f"[P{prio}] {task}" for task in tasks])
    return output

if __name__ == "__main__":
    task_sets = {3: ["Cleanup", "Optimize"], 1: ["Log"], 2: ["Validate", "Ping"]}
    print(multiplex_tasks(task_sets))
