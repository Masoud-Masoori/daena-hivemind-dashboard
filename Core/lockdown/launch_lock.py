import os

def engage_launch_lock():
    lock_file = "D:/Ideas/Daena/core/lockdown/launch.lock"
    with open(lock_file, "w") as f:
        f.write("locked")
    print(" Launch locked to prevent premature deployment.")

def release_launch_lock():
    lock_file = "D:/Ideas/Daena/core/lockdown/launch.lock"
    if os.path.exists(lock_file):
        os.remove(lock_file)
        print(" Launch lock released.")
