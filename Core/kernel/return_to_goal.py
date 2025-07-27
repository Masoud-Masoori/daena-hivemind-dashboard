def restore_checkpoint():
    import json
    with open("D:/Ideas/Daena/logs/goal_checkpoint.json") as f:
        ctx = json.load(f)
    print("[RETURN] Reloading mission:", ctx.get("goal"))
    return ctx
