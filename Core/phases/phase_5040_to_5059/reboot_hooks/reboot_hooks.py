# reboot_hooks.py
import os

class RebootHookManager:
    def __init__(self, hook_file="D:/Ideas/Daena/hooks/reboot.flag"):
        self.hook_file = hook_file

    def request_reboot(self):
        with open(self.hook_file, "w") as f:
            f.write("REBOOT_REQUESTED")
        print("[RebootHook] Reboot flag written.")

    def check_reboot(self):
        if os.path.exists(self.hook_file):
            print("[RebootHook] Reboot signal detected.")
            return True
        return False
