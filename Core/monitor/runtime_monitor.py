import time, psutil

def check_runtime():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    print(f"Runtime Monitor  CPU: {cpu}%, MEM: {mem}%")
    return cpu < 85 and mem < 85
