def escalation_level(severity, scope):
    if severity > 7 and scope == "global":
        return " Critical"
    elif severity > 4:
        return " Moderate"
    else:
        return " Low"
        
if __name__ == "__main__":
    print("[Escalation]:", escalation_level(8, "global"))
