def audit_loopback(response_log):
    if "loopback" in response_log.lower():
        print("Loopback condition detected  investigate origin flow.")
