# autonomous_tool_user.py

import subprocess

class AutonomousToolUser:
    def execute_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=30)
            return result.decode()
        except Exception as e:
            return f"Error: {e}"
