import time, uuid, json

class BaseAgent:
    def __init__(self, role, department):
        self.id = str(uuid.uuid4())
        self.role = role
        self.department = department
        self.status = "active"
        self.loop()

    def loop(self):
        while True:
            print(f"[{self.role}] Agent {self.id} scanning tasks...")
            time.sleep(10)
