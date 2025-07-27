def cloak_signal(signal):
    return f"[Cloaked]  <<{signal[::-1]}>>"

if __name__ == "__main__":
    print(cloak_signal("CONFIDENTIAL"))
