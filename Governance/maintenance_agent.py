from Core.agents.agent import Agent as BaseAgent
import threading, time

class MaintenanceAgent(BaseAgent):
    def __init__(self, name, bus, memory, config=None, watched_agents=None):
        super().__init__(name, bus, memory, config)
        # Start a background thread to monitor resources
        threading.Thread(target=self.resource_monitor, daemon=True).start()

    def handle_message(self, message):
        content = message.get("content", "") or ""
        print(f"[MaintenanceAgent] Received message: {content}")
        if "status" in content.lower():
            status = "All systems nominal (dummy status)."
            self.send_message(message.get("from", ""), f"StatusReport: {status}")

    def resource_monitor(self):
        while True:
            # Periodically check for tasks (dummy loop)
            time.sleep(60)
            current_hour = time.localtime().tm_hour
            if current_hour == 0:
                print("[MaintenanceAgent] Performing scheduled maintenance tasks...")
                # e.g., could offload backups or heavy jobs to cloud here
