# override_shield.py
class OverrideShield:
    def __init__(self):
        self.whitelisted_sources = ["DAENA_CORE", "FOUNDER", "ROOTLOCK"]

    def is_allowed(self, source):
        return source in self.whitelisted_sources

    def validate_override(self, source, command):
        if not self.is_allowed(source):
            return f" OVERRIDE BLOCKED from {source}: not trusted."
        return f" OVERRIDE ACCEPTED from {source}: {command}"
