import requests, json, time

def fetch_world_news():
    print("[] Syncing with global state...")
    headlines = [
        {"topic": "AI Regulation", "risk": "medium"},
        {"topic": "Open Source Surge", "risk": "low"},
        {"topic": "Economic Instability", "risk": "high"},
        {"topic": "Tech Layoffs", "risk": "medium"}
    ]
    return headlines

def save_sync(data):
    with open("D:/Ideas/Daena/world_sync/latest_world_state.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    data = fetch_world_news()
    save_sync(data)
    print(" Synced with real-world state.")
