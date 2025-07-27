rollback_queue = []

def enqueue_instruction(instruction):
    rollback_queue.append(instruction)

def rollback_last():
    if rollback_queue:
        last = rollback_queue.pop()
        print(f"Rolling back: {last}")
        return last
