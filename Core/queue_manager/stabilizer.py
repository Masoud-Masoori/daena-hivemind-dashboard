from queue import Queue

agent_queue = Queue()

def enqueue_task(task):
    if agent_queue.qsize() > 50:
        return "Queue overload  defer task"
    agent_queue.put(task)
    return "Task queued"
