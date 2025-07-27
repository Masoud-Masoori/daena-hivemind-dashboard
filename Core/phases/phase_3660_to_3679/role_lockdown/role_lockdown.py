# role_lockdown.py
locked_roles = set()

def lock_role(role):
    locked_roles.add(role)

def is_locked(role):
    return role in locked_roles

def unlock_role(role):
    locked_roles.discard(role)
