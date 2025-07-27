# rogue_damping.py

def dampen_rogue_intent(command_log):
    blacklist = ['self-destruct', 'terminate_all', 'wipe_memory']
    for entry in command_log:
        if any(banned in entry.lower() for banned in blacklist):
            print(f"[RogueDamping]  Rogue command detected: {entry}")
            return False
    return True
