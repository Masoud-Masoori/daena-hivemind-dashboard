import time

def visualize_timeline(events):
    for e in events:
        print(f"[{time.strftime('%H:%M:%S')}] {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    visualize_timeline(["Qwen Responded", "R2 Responded", "Yi Responded", "Final Decision Made"])
