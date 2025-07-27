def behavioral_throttle(agent, load):
    return {
        "agent": agent,
        "load": load,
        "throttle": True if load > 90 else False
    }

if __name__ == "__main__":
    print("[Throttle] A2:", behavioral_throttle("A2", 95))
