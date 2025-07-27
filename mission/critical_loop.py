import time
def launch_loop(core, threshold=0.95):
    while True:
        stable = core.evaluate()
        if stable >= threshold:
            print("Mission Go for Launch")
            break
        time.sleep(5)
