def escalation_trigger(triggered):
    return "ESCALATE " if triggered else "OK "

if __name__ == "__main__":
    print("[Escalation] Flag:", escalation_trigger(True))
