def verify_preflight(items):
    missing = [item for item, passed in items.items() if not passed]
    if missing:
        print(" Preflight check failed on:", missing)
        return False
    print(" Preflight checklist passed.")
    return True
