def strategic_override(command, risk_factor):
    if risk_factor > 0.8:
        print(f"Command '{command}' flagged as high-risk. Manual override required.")
        return False
    print(f"Command '{command}' approved by strategic layer.")
    return True
