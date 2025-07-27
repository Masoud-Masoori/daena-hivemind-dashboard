import time

def perception_loop(cycles):
    for i in range(cycles):
        print(f"[Perception ]: Scanning... Frame {i}")
        time.sleep(0.3)

if __name__ == "__main__":
    perception_loop(3)
