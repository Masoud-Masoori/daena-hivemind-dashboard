import json, time

def echo_sync(event):
    with open("core/sync/echo/echo_map.json", "r") as f:
        data = json.load(f)
    data["latest_sync"] = time.time()
    data["recent_events"].append(event)
    with open("core/sync/echo/echo_map.json", "w") as f:
        json.dump(data, f, indent=2)
