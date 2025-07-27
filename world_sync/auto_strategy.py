import json

def adjust_strategy():
    with open("D:/Ideas/Daena/world_sync/latest_world_state.json") as f:
        state = json.load(f)

    response = []
    for item in state:
        if item["risk"] == "high":
            suggestion = f"Immediate policy adjustment for {item['topic']}"
        elif item["risk"] == "medium":
            suggestion = f"Review and monitor {item['topic']}"
        else:
            suggestion = f"No immediate action needed for {item['topic']}"
        response.append(suggestion)

    with open("D:/Ideas/Daena/world_sync/strategy_response.json", "w") as f:
        json.dump(response, f, indent=2)
    print(" Strategic actions prepared.")

if __name__ == "__main__":
    adjust_strategy()
