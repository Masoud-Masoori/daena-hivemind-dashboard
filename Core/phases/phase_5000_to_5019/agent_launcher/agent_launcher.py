# agent_launcher.py
import subprocess

class AgentLauncher:
    def launch(self, agent_script):
        try:
            subprocess.Popen(["python", agent_script])
            print(f"[Launcher] {agent_script} launched.")
        except Exception as e:
            print(f"[Launcher Error] {e}")
