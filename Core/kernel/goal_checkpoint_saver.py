def save_goal_checkpoint(context):
    with open("D:/Ideas/Daena/logs/goal_checkpoint.json", "w") as f:
        import json; json.dump(context, f)
    print("[CHECKPOINT] Mission saved.")
