def relay_task(sender, receiver, task):
    print(f"[RELAY] {sender}  {receiver}: {task}")
    return {"status": "relayed", "to": receiver, "task": task}
