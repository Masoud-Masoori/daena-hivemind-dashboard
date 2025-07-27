# kernel_enforcer.py
class GovernanceKernel:
    def __init__(self, policies):
        self.policies = policies

    def enforce(self, action):
        for rule in self.policies:
            if not rule.validate(action):
                return f" Blocked by policy: {rule.reason}"
        return " Allowed"
