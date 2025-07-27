def recovery_hook(agent, last_state):
    return {
        "agent": agent,
        "restored_from": last_state,
        "tethered": True
    }

if __name__ == "__main__":
    print("[OverrideRecovery] ", recovery_hook("Echo", "memory_snapshot_142"))
