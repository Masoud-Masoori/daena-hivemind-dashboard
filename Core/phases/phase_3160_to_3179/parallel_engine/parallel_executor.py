# parallel_executor.py

import threading

def execute_parallel(tasks):
    threads = []
    for task in tasks:
        t = threading.Thread(target=task['fn'], args=task.get('args', ()))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("[Parallel] All tasks completed.")
