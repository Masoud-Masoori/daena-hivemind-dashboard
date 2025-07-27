def enforce_lock(reason="Unknown", level=3):
    print(f"[LOCK INITIATED] Reason: {reason} | Security Level: {level}")
    raise SystemExit("Locked by Daena Core Protocol.")
