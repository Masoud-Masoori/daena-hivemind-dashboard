# loop_detector.py

class DeepLoopDetector:
    def __init__(self):
        self.command_memory = {}

    def detect_loop(self, agent_id, command):
        history = self.command_memory.setdefault(agent_id, [])
        if len(history) > 10 and history[-5:] == [command] * 5:
            print(f"[LoopDetector]  Loop detected in agent {agent_id}  interrupting pattern.")
            return True
        history.append(command)
        return False
