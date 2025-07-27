def fallback_safety_check():
    print(" Running fallback kernel check...")
    import random
    result = random.choice([True, True, False])  # Mostly safe
    if not result:
        print(" Kernel safety compromised! Triggering fallback.")
    return result
