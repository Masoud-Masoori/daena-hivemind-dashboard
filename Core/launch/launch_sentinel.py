def watch_launch_status(systems):
    for name, status in systems.items():
        if status != "ready":
            print(f" Launch blocked: {name} not ready")
            return False
    print(" All systems GO.")
    return True
