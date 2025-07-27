def activate_failsafe(reason="Overload"):
    print(f"[FAILSAFE] Triggered due to: {reason}")
    # In real mode, notify user/admin or reboot
    return True
