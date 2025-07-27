def clarify_command(cmd):
    if "?" not in cmd and not cmd.strip().endswith("?"):
        return f"[Clarify]  Did you mean: '{cmd.strip()}?'"
    return f"[Clarify]  Understood: {cmd.strip()}"

if __name__ == "__main__":
    print(clarify_command("What is the agent status"))
