recovery_hooks = []

def register_hook(hook_func):
    recovery_hooks.append(hook_func)

def trigger_hooks():
    for hook in recovery_hooks:
        try:
            hook()
        except Exception as e:
            print(f"Recovery hook failed: {e}")
