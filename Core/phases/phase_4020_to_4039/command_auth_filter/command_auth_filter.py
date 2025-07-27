# command_auth_filter.py
class CommandAuthFilter:
    def __init__(self, allowed_users):
        self.allowed_users = allowed_users

    def validate(self, user, command):
        if user not in self.allowed_users:
            raise PermissionError(f"User {user} is not authorized for command: {command}")
        return True
