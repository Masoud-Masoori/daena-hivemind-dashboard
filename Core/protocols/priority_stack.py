priority_stack = []

def add_priority_task(task, level):
    priority_stack.append((level, task))
    priority_stack.sort(reverse=True)

def get_next_task():
    return priority_stack.pop() if priority_stack else None
