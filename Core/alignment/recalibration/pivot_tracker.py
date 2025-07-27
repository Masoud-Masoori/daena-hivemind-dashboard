last_checkpoint = ""

def update_checkpoint(task):
    global last_checkpoint
    last_checkpoint = task

def verify_continuity(current_task):
    return current_task.startswith(last_checkpoint[:10])
