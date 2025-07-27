def relay_error_to_dashboard(module, error_message):
    log = f"[{module}] ERROR -> {error_message}"
    print("Relay:", log)
    # In real-world: send to dashboard socket/channel
