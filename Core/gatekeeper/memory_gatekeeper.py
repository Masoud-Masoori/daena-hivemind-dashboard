def gatekeep_memory(usage_percent):
    if usage_percent > 85:
        print("Memory usage high  initiating cleanup...")
        return "cleanup_triggered"
    return "stable"
