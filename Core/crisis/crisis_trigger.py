def crisis_mode(status):
    if status == "critical":
        return "[CRISIS MODE]  Daena lockdown initiated"
    return "[NORMAL] System stable"

if __name__ == "__main__":
    print(crisis_mode("critical"))
