def reconfirm_command(command):
    confirmation = input(f"Reconfirm execution of: {command}? (yes/no): ")
    return confirmation.strip().lower() == "yes"
