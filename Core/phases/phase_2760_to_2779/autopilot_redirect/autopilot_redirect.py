# autopilot_redirect.py

import time

def redirect_to_backup(goal, backup_goal):
    print(f"[Autopilot]  Primary goal '{goal}' unreachable.")
    print(f"[Autopilot]  Redirecting to fallback plan: '{backup_goal}'")
    time.sleep(1)
    print(f"[Autopilot]  Now pursuing: {backup_goal}")
