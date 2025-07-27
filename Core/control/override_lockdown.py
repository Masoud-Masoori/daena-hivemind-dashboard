def enforce_lockdown(triggered):
    if triggered:
        return "[Lockdown]  Emergency Override Enabled"
    return "[Lockdown]  Normal Mode"

if __name__ == "__main__":
    print(enforce_lockdown(True))
