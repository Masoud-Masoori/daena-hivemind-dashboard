import time
def boot_departments():
    print(" Spinning up all departments...")
    departments = ["security", "cmp", "freelance", "analytics", "governance"]
    for d in departments:
        print(f" Department {d} online.")
        time.sleep(1)
