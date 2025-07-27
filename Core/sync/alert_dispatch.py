def dispatch_alert(department, level):
    if level > 5:
        return f"[ALERT]  Urgent ping to {department}"
    return f"[ALERT] ? Routine log to {department}"

if __name__ == "__main__":
    print(dispatch_alert("Legal", 7))
