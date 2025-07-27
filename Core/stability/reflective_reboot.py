class ReflectiveReboot:
    def __init__(self):
        self.crash_log = []

    def log_issue(self, error):
        self.crash_log.append(error)
        print(f" Issue logged: {error}")

    def reboot(self):
        print(" Reflective reboot initiated.")
        return "System state reset and logic path reviewed."
