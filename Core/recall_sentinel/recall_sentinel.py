command_memory = {}

def store_command(cmd_id, cmd_text):
    command_memory[cmd_id] = cmd_text

def retrieve_command(cmd_id):
    return command_memory.get(cmd_id, "Command not found")
