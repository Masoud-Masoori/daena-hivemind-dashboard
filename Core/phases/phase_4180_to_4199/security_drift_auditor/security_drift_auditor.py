# security_drift_auditor.py
class SecurityDriftAuditor:
    def __init__(self):
        self.baseline_permissions = {
            "read": True, "write": True, "delete": False, "launch_hidden": False
        }

    def audit(self, current_permissions):
        drift = {}
        for k, v in self.baseline_permissions.items():
            if current_permissions.get(k) != v:
                drift[k] = current_permissions.get(k)
        return drift
