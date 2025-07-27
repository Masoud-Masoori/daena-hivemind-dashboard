loop_memory = {}

def detect_loop(agent_id, command):
    history = loop_memory.get(agent_id, [])
    history.append(command)
    if history.count(command) > 3:
        print(f"[LoopDetector]  Detected potential loop for: {agent_id}  {command}")
        return True
    loop_memory[agent_id] = history[-10:]
    return False
