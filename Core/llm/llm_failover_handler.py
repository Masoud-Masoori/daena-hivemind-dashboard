def handle_failover(task):
    print("[FAILOVER] Using Reflex or DeepSeek fallback.")
    return "reflex" if "vision" not in task else "deepseek"
