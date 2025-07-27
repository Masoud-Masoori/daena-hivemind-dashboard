def handle_interrupt(signal):
    if signal in ("SIGINT", "SIGTERM"):
        return f"[InterruptHandler]  Received {signal}, performing safe shutdown."
    return "[InterruptHandler]  All clear."

if __name__ == "__main__":
    print(handle_interrupt("SIGINT"))
