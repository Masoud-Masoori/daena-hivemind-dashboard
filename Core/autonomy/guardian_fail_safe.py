import time, json

def monitor_agents():
    stuck_agents = []
    with open("D:\\Ideas\\Daena\\logs\\agent_log.jsonl") as f:
        for line in f.readlines()[-100:]:
            entry = json.loads(line)
            if entry.get("status") == "looping":
                stuck_agents.append(entry["agent"])
    if stuck_agents:
        alert = f" Stuck agents detected: {', '.join(stuck_agents)}"
        with open("D:\\Ideas\\Daena\\ui\\dashboard-react\\alerts.txt", "a") as f:
            f.write(alert + "\\n")
        # Optionally disable them
        print(alert)
        return True
    return False

while True:
    if monitor_agents():
        time.sleep(300)
    else:
        time.sleep(60)
